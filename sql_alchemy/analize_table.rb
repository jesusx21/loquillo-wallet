require('sequel')

module SQLAlchemy
  class TableAnalizer
    def initialize(db, table_name, table)
      @db = db
      @table_name = table_name
      @table = table
    end

    def analize
      if @db.find_tables.include? @table_name
        table_saved = @db.find_table_by_name(@table_name)

        schema = @db.find_table_schema(@table_name)
        return build_alter_table_migration(@table, schema)
      end

      build_add_table_migration
    end

    private

    def build_alter_table_migration(table, schema)
      migration = Migration.new table, :alter_table

      table.columns.each do |column|
        schema_column = schema.column_by_name(column.name)

        if schema_column.nil?
          migration.add_column(column)
          next
        end

        default = unless column.options[:default].nil?
          "#{column.options[:default]}()"
        else
          nil
        end

        unless migration.equal_column?(column, schema_column)
          if column.name != schema_column.name
            migration.rename_column(column.name, column.type)
          end

          if column.type != schema_column.type
            migration.set_column_type(column.name, schema_column.type, column.type)
          end

          if (column.options[:primary] || false) != schema_column.options[:primary_key]
            migration.add_primary_key(column.name)
          end

          if default != schema_column.options[:default]
            migration.set_column_default(column.name, schema_column.options[:default], default)
          end
        end
      end

      schema.columns.each do |schema_column|
        column = table.column_by_name(schema_column.name)

        if column.nil?
          migration.drop_column(schema_column)
        end
      end

      migration
    end

    def build_add_table_migration
      migration = Migration.new @table, :create_table

      @table.columns.each { |column| migration.add_column(column) }

      migration
    end
  end
end

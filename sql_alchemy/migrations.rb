module SQLAlchemy
  class Migrations
    def initialize(tables_path, schema)
      config = initialize_config()
      @db = Database.new(config)

      @db.init

      @tables_path = tables_path
      @schema = schema
    end

    def create(migration_name)
      tables_dir = Dir["#{@tables_path}/*.rb"]

      tables_dir.each do |table_dir|
        require_relative("../#{table_dir}")
      end

      load_tables @schema
      migrations = []

      @schema.tables.each do |table|
        migration = analize_table(table.name, table)

        migrations.push(migration) if migration.changes?
      rescue StandardError
        # pass
      end

      schema_tables = @schema.table_names
      @db.find_tables.each do |table_name|
        table = @db.find_table_by_name(table_name)

        unless schema_tables.include? table_name
          migration = Migration.new table, :drop_table
          migrations.push(migration) if migration.changes?
        end
      end

      build_migration_file(migrations)
      # @db.store_tables(@schema.tables)
    # rescue StandardError => error
    #   pp error
    end

    def run
      Sequel::Migrator.run(@db.connection, './migrations', column: :migrations)

      @db.run_changes
    rescue StandardError => error
      pp error
    end

    private

    def analize_table(table_name, table)
      table_analizer = TableAnalizer.new @db, table_name, table
      table_analizer.analize
    end

    def build_migration_file(migrations)
      file_string = "require('sequel')\n\nSequel.migration do\n"
      up_string = ""
      down_string = ""

      up_string_migrations = migrations.map do |migration|
        migration.build_up_string
      end

      down_string_migrations = migrations.reverse.map do |migration|
        migration.build_down_string
      end

      up_string = up_string_migrations.join("\n")
      down_string = down_string_migrations.join("\n")
      file_string += "\tup do\n#{up_string}\tend\n\n"
      file_string += "\tdown do\n#{down_string}\tend\n"

      file_string += "end"
      File.write("./migrations/#{Time.now.to_i}_create_users_table.rb", file_string)
    end


    def initialize_config
      {
        'adapter' => 'postgresql',
        'encoding' => 'utf-8',
        'host' => 'localhost',
        'port' => 5432,
        'database' => 'mr_krabz_dev',
        'username' => 'postgres'
      }
    end
  end
end

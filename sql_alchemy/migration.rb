module SQLAlchemy
  class Migration
    attr_reader :table, :type

    def initialize(table, type)
      @table = table
      @type = type

      @add_columns = []
      @alter_columns = []
      @drop_columns = []
    end

    def add_column(column)
      @add_columns.push(column)
    end

    def rename_column(previous_name, new_name)
      metadata = {
        previous_name: previous_name,
        new_name: new_name
      }

      alter_column(:rename_column, metadata)
    end

    def set_column_type(name, previous_type, new_type)
      metadata = {
        name: name,
        previous_type: previous_type,
        new_type: new_type
      }

      alter_column(:set_column_type, metadata)
    end

    def add_primary_key(name)
      metadata = {
        name: name
      }

      alter_column(:add_primary_key, metadata)
    end

    def set_column_default(name, previous_default, new_default)
      metadata = {
        name: name,
        previous_default: previous_default,
        new_default: new_default
      }

      alter_column(:set_column_default, metadata)
    end

    def alter_column(type, metadata)
      @alter_columns.push({
        type: type,
        metadata: metadata
      })
    end

    def drop_column(column)
      @drop_columns.push(column)
    end

    def equal_column?(column, schema_column)
      default = unless column.options[:default].nil?
        "#{column.options[:default]}()"
      else
        nil
      end

      column.name == schema_column.name  && \
        column.type == schema_column.type && \
        (column.options[:primary] || false) == schema_column.options[:primary_key] && \
        default == schema_column.options[:default]
    end

    def build_up_string
      if @type == :drop_table
       return "\t\tdrop_table :#{@table.name}\n"
      end

      result = "\t\t#{@type} :#{@table.name} do\n"

      unless @drop_columns.empty?
        result += drop_colums_as_s(@drop_columns)
      end

      unless @add_columns.empty?
        result += add_colums_as_s(@add_columns)
      end

      unless @alter_columns.empty?
        result += up_alter_columns_as_s
      end

      result += "\t\tend\n"

      result
    end

    def build_down_string
      type = if @type == :create_table
        :drop_table
      elsif @type == :drop_table
        :create_table
      else
        @type
      end

      if type == :drop_table
        return "\t\t#{type} :#{@table.name}\n"
      end

      if @type == :drop_table
        @table.columns.each { |column| drop_column(column) }
      end

      result = "\t\t#{type} :#{@table.name} do\n"

      unless @drop_columns.empty?
        result += add_colums_as_s @drop_columns
      end

      unless @add_columns.empty?
        result += drop_colums_as_s @add_columns
      end

      unless @alter_columns.empty?
        result += down_alter_columns_as_s
      end

      result += "\t\tend\n"

      result
    end

    def changes?
      @type != :alter_table || \
        !@add_columns.empty? || \
        !@alter_columns.empty? || \
        !@drop_columns.empty?
    end

    private

    def add_colums_as_s(columns_to_add)
      result = ""

      columns_to_add.each do |column|
        options = column.options
        type = map_types(column.type)

        default = if options[:default].is_a? Symbol
                    "Sequel.lit('#{options[:default].to_s}()')"
                  else
                    options[:default]
                  end

        if options[:primary]
          result += "\t\t\tprimary_key :#{column.name}, type: :#{type}"
        else
          result += "\t\t\t#{type} :#{column.name}" if @type == :create_table || @type == :drop_table
          result += "\t\t\tadd_column :#{column.name} type: :#{type}" if @type == :alter_table
        end

        result += ", null: #{options[:null]}" unless options[:null].nil?
        result += ", unique: #{options[:unique]}" unless options[:unique].nil?
        result += ", default: #{default}" unless default.nil? || options[:default].empty?
        result += "\n"
      end

      result
    end

    def up_alter_columns_as_s
      result = ""

      @alter_columns.each do |item|
        metadata = item[:metadata]

        if item[:type] == :rename_column
          result += "\t\t\trename_column :#{metadata[:previous_name]}, :#{metadata[:new_name]}\n"
        end

        if item[:type] == :set_column_type
          type = map_types(metadata[:new_type])
          result += "\t\t\tset_column_type :#{metadata[:name]}, #{type}\n"
        end

        if item[:type] == :add_primary_key
          result += "\t\t\tadd_primary_key :#{metadata[:name]}\n"
        end

        if item[:type] == :set_column_default
          result += "\t\t\tset_column_default :#{metadata[:name]}, Sequel.lit('#{metadata[:new_default]}()')\n"
        end
      end

      result
    end

    def down_alter_columns_as_s
      result = ""

      @alter_columns.reverse.each do |item|
        metadata = item[:metadata]

        if item[:type] == :rename_column
          result += "\t\t\trename_column :#{metadata[:new_name]}, :#{metadata[:previous_name]}\n"
        end

        if item[:type] == :set_column_type
          type = map_types(metadata[:previous_type])
          result += "\t\t\tset_column_type :#{metadata[:name]}, #{type}\n"
        end

        if item[:type] == :add_primary_key
          result += "\t\t\tdrop_column :#{metadata[:name]}\n"
        end

        if item[:type] == :set_column_default
          result += "\t\t\tset_column_default :#{metadata[:name]}, Sequel.lit('#{metadata[:previous_default]}()')\n"
        end
      end

      result
    end

    def drop_colums_as_s(columns)
      result = ""

      columns.each do |column|
        result += "\t\t\tdrop_column :#{column.name}\n"
      end

      result
    end

    def map_types(type)
      types = {
        primary_key: 'primary_key',
        string: 'String',
        datetime: 'DateTime',
        uuid: 'uuid',
        json: 'json'
      }

      types[type]
    end
  end
end

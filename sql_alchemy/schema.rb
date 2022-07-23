module SQLAlchemy
  class Schema
    def initialize
      @tables = {}
    end

    def add_table(table)
      @tables[table.name] = table.new
    end

    def table_names
      @tables.keys
    end

    def tables
      @tables.values
    end
  end
end

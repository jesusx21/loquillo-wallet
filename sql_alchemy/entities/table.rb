module SQLAlchemy::Entities
  class Table
    attr_reader :columns, :name

    def initialize(name, run = false)
      @name = name
      @run = run

      @columns = []
    end

    def last_migration_run?
      @run
    end

    def add_column(name, type, options = {})
      column = Column.new(name, type, options)

      @columns.push(column)
    end

    def column_by_name(name)
      @columns.select { |column| column.name == name }
        .first
    end

    private

    def timestamps(*args)
      args.each do |field_name|
        add_column(field_name, :datetime, default: :now)
      end
    end
  end
end

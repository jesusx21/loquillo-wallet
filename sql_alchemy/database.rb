module SQLAlchemy
  MIGRATION_TABLES = [:db_schema_tables, :db_schema_columns, :schema_migrations].freeze

  class Database
    attr_reader :connection

    def initialize(config)
      @connection = connect(config)
    end

    def find_tables
      @connection.tables.select do |table_name|
        !MIGRATION_TABLES.include? table_name
      end
    end

    def init
      create_migrations_tables
      @connection.run 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'
    end

    def store_migration(table_name, table)
      table_id = @connection[:db_schema_tables]
                 .insert(name: table_name.to_s)

      table.columns.each do |column|
        @connection[:db_schema_columns]
          .insert(
            table_id: table_id,
            name: column.name.to_s,
            is_primary_key: column.options[:primary] || false,
            default: column.options[:default].to_s,
            type: column.type.to_s
          )
      end
    end

    def add_table(table)
      table_id = @connection[:db_schema_tables]
                .insert(name: table.name.to_s)

      table.columns.each do |column|
        @connection[:db_schema_columns]
          .insert(
            table_id: table_id,
            name: column.name.to_s,
            is_primary_key: column.options[:primary] || false,
            default: column.options[:default].to_s,
            type: column.type.to_s
          )
      end
    end

    def update_table(table)
      table = @connection[:db_schema_tables]
                .returning(Sequel.lit)
                .where(name: table.name.to_s)
                .update(run: false)

      @connection[:db_schema_columns]
        .where(table_id: table[:id])
        .delete

      table.columns.each do |column|
        @connection[:db_schema_columns]
          .insert(
            table_id: table_id,
            name: column.name.to_s,
            is_primary_key: column.options[:primary] || false,
            default: column.options[:default].to_s,
            type: column.type.to_s
          )
      end
    end

    def delete_table

    end

    def find_table_by_name(name)
      table_data = @connection[:db_schema_tables]
        .where(name: name.to_s)
        .first

      if (table_data.nil?)
        raise StandardError, 'table not found'
      end

      table = Entities::Table.new(table_data[:name], table_data[:run])

      columns_data = @connection[:db_schema_columns]
        .where(table_id: table_data[:id])
        .all

      columns_data.each do |item|

        table.add_column(
          item[:name].to_sym,
          item[:type].to_sym,
          {
            primary: item[:is_primary_key],
            default: item[:default]&.to_sym,
            unique: item[:unique],
            run: item[:run]
          }
        )
      end

      table
    end

    def run_changes
      @connection[:db_schema_columns]
        .where(run: false)
        .update(run: true)

      @connection[:db_schema_tables]
        .where(run: false)
        .update(run: true)
    end

    def find_table_schema(name)
      result = @connection.schema(name)
      schema = Entities::Schema.new(name)

      result.each do |item|
        type = (item[1][:type] || item[1][:db_type]).to_sym
        options = {
          default: item[1][:default],
          allow_null: item[1][:allow_null],
          primary_key: item[1][:primary_key]
        }

        schema.add_column(item[0].to_sym, type, options)
      end

      schema
    end

    private

    def create_migrations_tables
      current_tables = @connection.tables

      unless current_tables.include? :db_schema_tables
        create_schema_table
      end

      unless current_tables.include? :db_schema_columns
        create_schema_columns
      end
    end

    def connect(config)
      Sequel
        .connect(
          database_dsn(config),
          max_connections: config[:maximum_connections]
        )
        .extension(:pagination)
    end

    def database_dsn(config)
      adapter = config['adapter']
      host = config['host']
      port = config['port']
      database = config['database']
      user = config['username']
      password = config['password']

      uri = "#{adapter}://"
      uri += "#{user}:#{password}@" unless user.nil?
      uri += host.to_s
      uri += ":#{port}" unless port.nil?
      uri += "/#{database}"

      uri.freeze
    end

    def create_schema_table
      @connection.create_table :db_schema_tables do
        primary_key :id, Bignum
        String :name, null: false
        Boolean :run, default: false

        index :name, unique: true
      end
    end

    def create_schema_columns
      @connection.create_table :db_schema_columns do
        foreign_key :table_id, :db_schema_tables
        String :name, null: false
        Boolean :is_primary_key
        Boolean :run, default: false
        String :default
        String :type

        primary_key([:table_id, :name])
      end
    end
  end
end

module Tables
  class Wallets < SQLAlchemy::Entities::Table
    def initialize
      super(:wallets)

      add_column(:ids, :uuid, primary: true, default: :uuid_generate_v4)
      add_column(:name, :string, unique: true)
      add_column(:currency, :string)

      timestamps(:created_at, :updated_at)
    end

    def self.name
      :wallets
    end
  end
end

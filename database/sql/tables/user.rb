module Tables
  class Users < SQLAlchemy::Entities::Table
    def initialize
      super(:users)

      add_column(:ids, :uuid, primary: true, default: :uuid_generate_v4)
      add_column(:name, :json)
      add_column(:email, :string, unique: true)
      add_column(:password, :json)

      timestamps(:created_at, :updated_at)
    end

    def self.name
      :users
    end
  end
end

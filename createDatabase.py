import sqlite3
conn = sqlite3.connect('bi_lmparts.db')

cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    value REAL,
    cost REAL,
    code TEXT,
    barcode TEXT,
    available_stock INTEGER,
    ncm_code TEXT,
    cest_code TEXT,
    net_weight REAL,
    gross_weight REAL,
    category_id TEXT,
    unit_measure TEXT,
    FOREIGN KEY (category_id) REFERENCES categorias(id)
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    company_name TEXT,
    email TEXT,
    business_phone TEXT,
    mobile_phone TEXT,
    person_type TEXT,
    document TEXT,
    identity_document TEXT,
    state_registration_number TEXT,
    state_registration_type TEXT,
    city_registration_number TEXT,
    date_of_birth TEXT,
    notes TEXT,
    created_at TEXT
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS enderecos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id TEXT,
    street TEXT,
    number TEXT,
    complement TEXT,
    zip_code TEXT,
    neighborhood TEXT,
    city_name TEXT,
    state_name TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS contas_financeiras (
    uuid TEXT PRIMARY KEY,
    name TEXT,
    accountType TEXT,
    billetConfigured BOOLEAN
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS vendedores (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id TEXT PRIMARY KEY,
    contaAzulId INTEGER,
    number INTEGER,
    emission TEXT,
    status TEXT,
    scheduled BOOLEAN,
    customer_id TEXT,
    discount_measure_unit TEXT,
    discount_rate REAL,
    payment_type TEXT,
    payment_method TEXT,
    financial_account_id TEXT,
    notes TEXT,
    shipping_cost REAL,
    total REAL,
    seller_id TEXT,
    FOREIGN KEY (customer_id) REFERENCES clientes(id),
    FOREIGN KEY (seller_id) REFERENCES vendedores(id),
    FOREIGN KEY (financial_account_id) REFERENCES contas_financeiras(uuid)
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS itens_vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    value REAL
);
''')

conn.commit()

cur.execute('''
CREATE TABLE IF NOT EXISTS parcelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id TEXT,
    number INTEGER,
    value REAL,
    due_date TEXT,
    status TEXT,
    note TEXT,
    hasBillet BOOLEAN,
    FOREIGN KEY (venda_id) REFERENCES vendas(id)
);
''')

conn.commit()

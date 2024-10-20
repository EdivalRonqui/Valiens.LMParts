# CREATE TABLES
create_Categorias = '''
    CREATE TABLE IF NOT EXISTS categorias (
        id TEXT PRIMARY KEY,
        uuid TEXT NOT NULL, 
        code TEXT NOT NULL,
        description TEXT NOT NULL,
        type TEXT NOT NULL, 
        level INTEGER, 
        feedDRECost NUMERIC, 
        accountancyCodeBlocked NUMERIC,
        hasBlockedStatements NUMERIC 
        configurable NUMERIC, 
        hasPendingConfiguration NUMERIC, 
        hasChildren NUMERIC, 
        financeAccountId REAL,
        financeAccountDescription TEXT, 
        parentLedgerAccountId TEXT, 
        isReprocessing TEXT, 
        accountancyCode TEXT, 
        accountancyCodeDescription TEXT, 
        accountancyRuleDescription TEXT, 
        originsOfAccountancyEvents TEXT, 
        accountancyAccount TEXT, 
        id_empresa TEXT

    );
    '''

create_CentroCustos = '''
    CREATE TABLE IF NOT EXISTS centrocustos (
        id TEXT PRIMARY KEY,
        version INTEGER NOT NULL,
        code TEXT NULL,
        name TEXT NOT NULL,
        parent TEXT NULL,
        active TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id)
    );
    '''

create_Clientes = '''
    CREATE TABLE IF NOT EXISTS clientes (
        uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        document TEXT,
        personType TEXT,
        profiles TEXT,
        active TEXT,
        email TEXT,
        phone TEXT,
        personLegacyId TEXT,
        personLegacyUUID TEXT,
        id_empresa TEXT NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id)
    );
    '''

create_ContasPagar = '''
    CREATE TABLE IF NOT EXISTS contaspagar (
        id TEXT NOT NULL,
        acquittanceScheduled TEXT NULL,
        attachment TEXT NULL,
        authorizedBankSlipId TEXT NULL,
        categoryId TEXT NULL,
        chargeRequest INTEGER NULL,
        conciliated TEXT NOT NULL,
        description TEXT NOT NULL,
        dueDate TEXT NOT NULL,
        expectedPaymentDate TEXT NOT NULL,
        financialAccount_cashierAccount TEXT NOT NULL,
        financialAccount_contaAzulDigital TEXT NOT NULL,
        financialAccount_id TEXT NOT NULL,
        financialAccount_type TEXT NOT NULL,
        financialEvent_categoryCount TEXT NOT NULL,
        financialEvent_categoryDescriptions TEXT NOT NULL,
        financialEvent_competenceDate TEXT NOT NULL,
        financialEvent_costCenterCount TEXT NOT NULL,
        financialEvent_description TEXT NOT NULL,
        financialEvent_id TEXT NOT NULL,
        financialEvent_negotiator_id TEXT NOT NULL,
        financialEvent_negotiator_name TEXT NOT NULL,
        financialEvent_numberOfInstallments TEXT NOT NULL,
        financialEvent_recurrenceIndex TEXT NOT NULL,
        financialEvent_reference_id TEXT NOT NULL,
        financialEvent_reference_origin TEXT NOT NULL,
        financialEvent_reference_revision TEXT NOT NULL,
        financialEvent_scheduled TEXT NOT NULL,
        financialEvent_type TEXT NOT NULL,
        financialEvent_value TEXT NOT NULL,
        financialEvent_version TEXT NOT NULL,
        fk_categoria TEXT NOT NULL,
        hasDigitalReceipt TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        [index] INTEGER NOT NULL,
        lastAcquittanceDate TEXT NOT NULL,
        loss INTEGER NOT NULL,
        note INTEGER NOT NULL,
        paid FLOAT NOT NULL,
        paymentRequest TEXT NOT NULL,
        recurrent TEXT NOT NULL,
        reference INTEGER NOT NULL,
        status TEXT NOT NULL,
        totalNetValue FLOAT NOT NULL,
        unpaid FLOAT NOT NULL,
        valueCategory FLOAT NOT NULL,
        valueComposition_discount FLOAT NOT NULL,
        valueComposition_fee FLOAT NOT NULL,
        valueComposition_fine FLOAT NOT NULL,
        valueComposition_grossValue FLOAT NOT NULL,
        valueComposition_interest FLOAT NOT NULL,
        valueComposition_netValue FLOAT NOT NULL,
        version INTEGER NOT NULL,
        categoryValue FLOAT NOT NULL,
        costCenterId TEXT NOT NULL,
        costCenterValue FLOAT NOT NULL,
        valor_lancamento FLOAT NOT NULL,
        fk_centroCusto TEXT NOT NULL,
        FOREIGN KEY (categoryId) REFERENCES categorias(id),
        FOREIGN KEY (id_empresa) REFERENCES empresas(id),
        FOREIGN KEY (costCenterId) REFERENCES centro_custos(id)
    );
    '''

create_ContasReceber = '''
    CREATE TABLE IF NOT EXISTS contasreceber (
        id TEXT NOT NULL,
        acquittanceScheduled TEXT NULL,
        attachment TEXT NULL,
        authorizedBankSlipId TEXT NULL,
        categoryId TEXT NULL,
        chargeRequest INTEGER NULL,
        conciliated TEXT NOT NULL,
        description TEXT NOT NULL,
        dueDate TEXT NOT NULL,
        expectedPaymentDate TEXT NOT NULL,
        financialAccount_cashierAccount TEXT NOT NULL,
        financialAccount_contaAzulDigital TEXT NOT NULL,
        financialAccount_id TEXT NOT NULL,
        financialAccount_type TEXT NOT NULL,
        financialEvent_categoryCount TEXT NOT NULL,
        financialEvent_categoryDescriptions TEXT NOT NULL,
        financialEvent_competenceDate TEXT NOT NULL,
        financialEvent_costCenterCount TEXT NOT NULL,
        financialEvent_description TEXT NOT NULL,
        financialEvent_id TEXT NOT NULL,
        financialEvent_negotiator_id TEXT NOT NULL,
        financialEvent_negotiator_name TEXT NOT NULL,
        financialEvent_numberOfInstallments TEXT NOT NULL,
        financialEvent_recurrenceIndex TEXT NOT NULL,
        financialEvent_reference_id TEXT NOT NULL,
        financialEvent_reference_origin TEXT NOT NULL,
        financialEvent_reference_revision TEXT NOT NULL,
        financialEvent_scheduled TEXT NOT NULL,
        financialEvent_type TEXT NOT NULL,
        financialEvent_value TEXT NOT NULL,
        financialEvent_version TEXT NOT NULL,
        fk_categoria TEXT NOT NULL,
        hasDigitalReceipt TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        [index] INTEGER NOT NULL,
        lastAcquittanceDate TEXT NOT NULL,
        loss INTEGER NOT NULL,
        note INTEGER NOT NULL,
        paid FLOAT NOT NULL,
        paymentRequest TEXT NOT NULL,
        recurrent TEXT NOT NULL,
        reference INTEGER NOT NULL,
        status TEXT NOT NULL,
        totalNetValue FLOAT NOT NULL,
        unpaid FLOAT NOT NULL,
        valueCategory FLOAT NOT NULL,
        valueComposition_discount FLOAT NOT NULL,
        valueComposition_fee FLOAT NOT NULL,
        valueComposition_fine FLOAT NOT NULL,
        valueComposition_grossValue FLOAT NOT NULL,
        valueComposition_interest FLOAT NOT NULL,
        valueComposition_netValue FLOAT NOT NULL,
        version INTEGER NOT NULL,
        categoryValue FLOAT NOT NULL,
        costCenterId TEXT NOT NULL,
        costCenterValue FLOAT NOT NULL,
        valor_lancamento FLOAT NOT NULL,
        fk_centroCusto TEXT NOT NULL,
        FOREIGN KEY (categoryId) REFERENCES categorias(id),
        FOREIGN KEY (id_empresa) REFERENCES empresas(id),
        FOREIGN KEY (costCenterId) REFERENCES centro_custos(id)
    );
    '''

create_Empresas = '''
    CREATE TABLE IF NOT EXISTS vendedores (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    '''

create_Vendas = '''
    CREATE TABLE IF NOT EXISTS vendas (
        tipo TEXT NOT NULL,
        numero TEXT NOT NULL,
        id_categoria TEXT NOT NULL,
        data TEXT NOT NULL,
        status TEXT NOT NULL,
        fatura_status TEXT NOT NULL,
        fatura_tipo_alerta TEXT NOT NULL,
        fatura_titulo_alerta TEXT NOT NULL,
        fatura_mensagem_alerta TEXT NOT NULL,
        fatura_tipo TEXT NOT NULL,
        configuracao_desconto_tipo TEXT NOT NULL,
        configuracao_desconto_taxa TEXT NOT NULL,
        composicao_valor_bruto FLOAT NOT NULL,
        composicao_valor_desconto FLOAT NOT NULL,
        composicao_valor_frete FLOAT NOT NULL,
        composicao_valor_impostos FLOAT NOT NULL,
        composicao_valor_seguro FLOAT NOT NULL,
        composicao_valor_liquido FLOAT NOT NULL,
        negociador_uuid TEXT NOT NULL,
        evento_financeiro_descricao TEXT NOT NULL,
        evento_financeiro_tipo TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor FLOAT NOT NULL,
        id_item_vendido TEXT NOT NULL,
        id_item_vendido_legado TEXT NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id)
    );
    '''

create_Servicos = '''
    CREATE TABLE IF NOT EXISTS servicos (
        id TEXT NOT NULL,
        serviceId TEXT NOT NULL,
        description TEXT NOT NULL,
        cost FLOAT NOT NULL,
        status TEXT NOT NULL,
        serviceType TEXT NOT NULL,
        taxScenarioList TEXT NOT NULL,
        price FLOAT NOT NULL,
        id_empresa TEXT NOT NULL,
        pk_produto TEXT NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id)
    );
    '''



# INSERT TABLES
insert_Categorias = '''
    INSERT INTO categorias (
        id,
        uuid,
        code,
        description,
        type,
        level,
        feedDRECost,
        accountancyCodeBlocked,
        hasBlockedStatements,
        NUMERIC,
        hasPendingConfiguration,
        hasChildren,
        financeAccountId,
        financeAccountDescription,
        parentLedgerAccountId,
        isReprocessing,
        accountancyCode,
        accountancyCodeDescription,
        accountancyRuleDescription,
        originsOfAccountancyEvents,
        accountancyAccount,
        id_empresa
    )
    VALUES (
        'id:TEXT',
        'uuid:TEXT',
        'code:TEXT',
        'description:TEXT',
        'type:TEXT',
        level:INTEGER,
        feedDRECost:NUMERIC,
        accountancyCodeBlocked:NUMERIC,
        'hasBlockedStatements:',
        'NUMERIC:configurable NUMERIC',
        hasPendingConfiguration:NUMERIC,
        hasChildren:NUMERIC,
        financeAccountId:REAL,
        'financeAccountDescription:TEXT',
        'parentLedgerAccountId:TEXT',
        'isReprocessing:TEXT',
        'accountancyCode:TEXT',
        'accountancyCodeDescription:TEXT',
        'accountancyRuleDescription:TEXT',
        'originsOfAccountancyEvents:TEXT',
        'accountancyAccount:TEXT',
        'id_empresa:TEXT'
    );
    '''

insert_CentroCustos = '''
    CREATE TABLE IF NOT EXISTS centrocustos (
        id TEXT PRIMARY KEY,
        version INTEGER NOT NULL,
        code TEXT NULL,
        name TEXT NOT NULL,
        parent TEXT NULL,
        active TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id)
    );
    '''

insert_Clientes = '''
    CREATE TABLE IF NOT EXISTS clientes (
        uuid TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        document TEXT,
        personType TEXT,
        profiles TEXT,
        active TEXT,
        email TEXT,
        phone TEXT,
        personLegacyId TEXT,
        personLegacyUUID TEXT,
        id_empresa TEXT NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id)
    );
    '''

insert_ContasPagar = '''
    CREATE TABLE IF NOT EXISTS contaspagar (
        id TEXT NOT NULL,
        acquittanceScheduled TEXT NULL,
        attachment TEXT NULL,
        authorizedBankSlipId TEXT NULL,
        categoryId TEXT NULL,
        chargeRequest INTEGER NULL,
        conciliated TEXT NOT NULL,
        description TEXT NOT NULL,
        dueDate TEXT NOT NULL,
        expectedPaymentDate TEXT NOT NULL,
        financialAccount_cashierAccount TEXT NOT NULL,
        financialAccount_contaAzulDigital TEXT NOT NULL,
        financialAccount_id TEXT NOT NULL,
        financialAccount_type TEXT NOT NULL,
        financialEvent_categoryCount TEXT NOT NULL,
        financialEvent_categoryDescriptions TEXT NOT NULL,
        financialEvent_competenceDate TEXT NOT NULL,
        financialEvent_costCenterCount TEXT NOT NULL,
        financialEvent_description TEXT NOT NULL,
        financialEvent_id TEXT NOT NULL,
        financialEvent_negotiator_id TEXT NOT NULL,
        financialEvent_negotiator_name TEXT NOT NULL,
        financialEvent_numberOfInstallments TEXT NOT NULL,
        financialEvent_recurrenceIndex TEXT NOT NULL,
        financialEvent_reference_id TEXT NOT NULL,
        financialEvent_reference_origin TEXT NOT NULL,
        financialEvent_reference_revision TEXT NOT NULL,
        financialEvent_scheduled TEXT NOT NULL,
        financialEvent_type TEXT NOT NULL,
        financialEvent_value TEXT NOT NULL,
        financialEvent_version TEXT NOT NULL,
        fk_categoria TEXT NOT NULL,
        hasDigitalReceipt TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        [index] INTEGER NOT NULL,
        lastAcquittanceDate TEXT NOT NULL,
        loss INTEGER NOT NULL,
        note INTEGER NOT NULL,
        paid FLOAT NOT NULL,
        paymentRequest TEXT NOT NULL,
        recurrent TEXT NOT NULL,
        reference INTEGER NOT NULL,
        status TEXT NOT NULL,
        totalNetValue FLOAT NOT NULL,
        unpaid FLOAT NOT NULL,
        valueCategory FLOAT NOT NULL,
        valueComposition_discount FLOAT NOT NULL,
        valueComposition_fee FLOAT NOT NULL,
        valueComposition_fine FLOAT NOT NULL,
        valueComposition_grossValue FLOAT NOT NULL,
        valueComposition_interest FLOAT NOT NULL,
        valueComposition_netValue FLOAT NOT NULL,
        version INTEGER NOT NULL,
        categoryValue FLOAT NOT NULL,
        costCenterId TEXT NOT NULL,
        costCenterValue FLOAT NOT NULL,
        valor_lancamento FLOAT NOT NULL,
        fk_centroCusto TEXT NOT NULL,
        FOREIGN KEY (categoryId) REFERENCES categorias(id),
        FOREIGN KEY (id_empresa) REFERENCES empresas(id),
        FOREIGN KEY (costCenterId) REFERENCES centro_custos(id)
    );
    '''

insert_ContasReceber = '''
    CREATE TABLE IF NOT EXISTS contasreceber (
        id TEXT NOT NULL,
        acquittanceScheduled TEXT NULL,
        attachment TEXT NULL,
        authorizedBankSlipId TEXT NULL,
        categoryId TEXT NULL,
        chargeRequest INTEGER NULL,
        conciliated TEXT NOT NULL,
        description TEXT NOT NULL,
        dueDate TEXT NOT NULL,
        expectedPaymentDate TEXT NOT NULL,
        financialAccount_cashierAccount TEXT NOT NULL,
        financialAccount_contaAzulDigital TEXT NOT NULL,
        financialAccount_id TEXT NOT NULL,
        financialAccount_type TEXT NOT NULL,
        financialEvent_categoryCount TEXT NOT NULL,
        financialEvent_categoryDescriptions TEXT NOT NULL,
        financialEvent_competenceDate TEXT NOT NULL,
        financialEvent_costCenterCount TEXT NOT NULL,
        financialEvent_description TEXT NOT NULL,
        financialEvent_id TEXT NOT NULL,
        financialEvent_negotiator_id TEXT NOT NULL,
        financialEvent_negotiator_name TEXT NOT NULL,
        financialEvent_numberOfInstallments TEXT NOT NULL,
        financialEvent_recurrenceIndex TEXT NOT NULL,
        financialEvent_reference_id TEXT NOT NULL,
        financialEvent_reference_origin TEXT NOT NULL,
        financialEvent_reference_revision TEXT NOT NULL,
        financialEvent_scheduled TEXT NOT NULL,
        financialEvent_type TEXT NOT NULL,
        financialEvent_value TEXT NOT NULL,
        financialEvent_version TEXT NOT NULL,
        fk_categoria TEXT NOT NULL,
        hasDigitalReceipt TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        [index] INTEGER NOT NULL,
        lastAcquittanceDate TEXT NOT NULL,
        loss INTEGER NOT NULL,
        note INTEGER NOT NULL,
        paid FLOAT NOT NULL,
        paymentRequest TEXT NOT NULL,
        recurrent TEXT NOT NULL,
        reference INTEGER NOT NULL,
        status TEXT NOT NULL,
        totalNetValue FLOAT NOT NULL,
        unpaid FLOAT NOT NULL,
        valueCategory FLOAT NOT NULL,
        valueComposition_discount FLOAT NOT NULL,
        valueComposition_fee FLOAT NOT NULL,
        valueComposition_fine FLOAT NOT NULL,
        valueComposition_grossValue FLOAT NOT NULL,
        valueComposition_interest FLOAT NOT NULL,
        valueComposition_netValue FLOAT NOT NULL,
        version INTEGER NOT NULL,
        categoryValue FLOAT NOT NULL,
        costCenterId TEXT NOT NULL,
        costCenterValue FLOAT NOT NULL,
        valor_lancamento FLOAT NOT NULL,
        fk_centroCusto TEXT NOT NULL,
        FOREIGN KEY (categoryId) REFERENCES categorias(id),
        FOREIGN KEY (id_empresa) REFERENCES empresas(id),
        FOREIGN KEY (costCenterId) REFERENCES centro_custos(id)
    );
    '''

insert_Empresas = '''
    CREATE TABLE IF NOT EXISTS vendedores (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    '''

insert_Vendas = '''
    CREATE TABLE IF NOT EXISTS vendas (
        tipo TEXT NOT NULL,
        numero TEXT NOT NULL,
        id_categoria TEXT NOT NULL,
        data TEXT NOT NULL,
        status TEXT NOT NULL,
        fatura_status TEXT NOT NULL,
        fatura_tipo_alerta TEXT NOT NULL,
        fatura_titulo_alerta TEXT NOT NULL,
        fatura_mensagem_alerta TEXT NOT NULL,
        fatura_tipo TEXT NOT NULL,
        configuracao_desconto_tipo TEXT NOT NULL,
        configuracao_desconto_taxa TEXT NOT NULL,
        composicao_valor_bruto FLOAT NOT NULL,
        composicao_valor_desconto FLOAT NOT NULL,
        composicao_valor_frete FLOAT NOT NULL,
        composicao_valor_impostos FLOAT NOT NULL,
        composicao_valor_seguro FLOAT NOT NULL,
        composicao_valor_liquido FLOAT NOT NULL,
        negociador_uuid TEXT NOT NULL,
        evento_financeiro_descricao TEXT NOT NULL,
        evento_financeiro_tipo TEXT NOT NULL,
        id_empresa TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor FLOAT NOT NULL,
        id_item_vendido TEXT NOT NULL,
        id_item_vendido_legado TEXT NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES categorias(id)
    );
    '''

insert_Servicos = '''
    CREATE TABLE IF NOT EXISTS servicos (
        id TEXT NOT NULL,
        serviceId TEXT NOT NULL,
        description TEXT NOT NULL,
        cost FLOAT NOT NULL,
        status TEXT NOT NULL,
        serviceType TEXT NOT NULL,
        taxScenarioList TEXT NOT NULL,
        price FLOAT NOT NULL,
        id_empresa TEXT NOT NULL,
        pk_produto TEXT NOT NULL,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id)
    );
    '''


# SELECT DATA
select_MaxContasPagar = '''
    SELECT MAX(dueDate) as lastDate from contaspagar;
    '''

select_MaxContasReceber = '''
    SELECT MAX(dueDate) as lastDate from contasreceber;
    '''

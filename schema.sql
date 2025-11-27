-- =====================================
-- ELIMINAR TABLAS SI EXISTEN (OPCIONAL)
-- =====================================
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PEDIDO_EN_LOCAL CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PEDIDO_PARA_LLEVAR CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PEDIDO_DESPACHO CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PEDIDO CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE CLIENTE CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- ======================
-- TABLA CLIENTE
-- ======================
CREATE TABLE CLIENTE (
    id_cliente NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    telefono VARCHAR2(20),
    correo VARCHAR2(100)
);

-- ======================
-- TABLA PEDIDO (PADRE)
-- ======================
CREATE TABLE PEDIDO (
    numeroPedido NUMBER PRIMARY KEY,
    id_cliente NUMBER NOT NULL,
    fecha DATE,
    totalPagar NUMBER(10,2),

    CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente)
        REFERENCES CLIENTE(id_cliente)
);

-- ==============================
-- TABLA PEDIDO EN LOCAL
-- ==============================
CREATE TABLE PEDIDO_EN_LOCAL (
    numeroPedido NUMBER PRIMARY KEY,
    numeroMesa NUMBER,

    CONSTRAINT fk_pedido_local FOREIGN KEY (numeroPedido)
        REFERENCES PEDIDO(numeroPedido)
        ON DELETE CASCADE
);

-- ==================================
-- TABLA PEDIDO PARA LLEVAR
-- ==================================
CREATE TABLE PEDIDO_PARA_LLEVAR (
    numeroPedido NUMBER PRIMARY KEY,
    tiempoEstimadoRetiro VARCHAR2(50),

    CONSTRAINT fk_pedido_llevar FOREIGN KEY (numeroPedido)
        REFERENCES PEDIDO(numeroPedido)
        ON DELETE CASCADE
);

-- ===============================
-- TABLA PEDIDO DESPACHO
-- ===============================
CREATE TABLE PEDIDO_DESPACHO (
    numeroPedido NUMBER PRIMARY KEY,
    direccion VARCHAR2(200),

    CONSTRAINT fk_pedido_despacho FOREIGN KEY (numeroPedido)
        REFERENCES PEDIDO(numeroPedido)
        ON DELETE CASCADE
);

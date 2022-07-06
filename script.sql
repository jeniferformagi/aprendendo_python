CREATE SCHEMA IF NOT EXISTS norktown;

CREATE TABLE IF NOT EXISTS norktown.pessoa (
	PEScpf varchar(11) NOT NULL,
	PESnome varchar(60) NOT NULL,
	PRIMARY KEY(PEScpf)
);

CREATE TABLE IF NOT EXISTS norktown.veiculo (
	VEIid integer NOT NULL,
	VEInome varchar(40) NOT NULL,
	VEIcor smallint NOT NULL,
	VEItipo smallint NOT NULL,
	PEScpf varchar(11) NOT NULL,
	PRIMARY KEY(VEIid, PEScpf),
	FOREIGN KEY (PEScpf) REFERENCES norktown.pessoa (PEScpf) ON DELETE CASCADE,
	CONSTRAINT ck_cor CHECK (VEIcor in (1, 2, 3)),
	CONSTRAINT ck_tipo CHECK (VEItipo in (1, 2, 3))
);

INSERT INTO norktown.pessoa VALUES ('10283127929', 'Jenifer Camila Formagi');
INSERT INTO norktown.pessoa VALUES ('36773050049', 'Roberto da Silva');
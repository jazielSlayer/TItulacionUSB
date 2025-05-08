-- Creando la base de datos para el sistema de gestión de titulación
CREATE DATABASE IF NOT EXISTS SistemaTitulacion;
USE SistemaTitulacion;

-- Tabla para almacenar información de los estudiantes
CREATE TABLE Estudiantes (
    IdEstudiante INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    CodigoEstudiante VARCHAR(20) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15),
    EstadoPagos TINYINT NOT NULL DEFAULT 0, -- 1: Al día, 0: Pendiente
    HabilitadoTitulacion TINYINT NOT NULL DEFAULT 0 -- 1: Habilitado, 0: No habilitado
) ENGINE=InnoDB;

-- Tabla para almacenar información de los docentes
CREATE TABLE Docentes (
    IdDocente INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15),
    Habilidades VARCHAR(500),
    HabilitadoGuia TINYINT NOT NULL DEFAULT 0, -- 1: Puede ser guía, 0: No puede
    EsJurado TINYINT NOT NULL DEFAULT 0 -- 1: Es jurado, 0: No es jurado
) ENGINE=InnoDB;

-- Tabla para los talleres
CREATE TABLE Talleres (
    IdTaller INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL, -- Taller 1 o Taller 2
    DuracionMeses INT NOT NULL DEFAULT 6,
    Descripcion VARCHAR(200)
) ENGINE=InnoDB;

-- Tabla para registrar la cursada de talleres por estudiante
CREATE TABLE EstudianteTalleres (
    IdEstudianteTaller INT PRIMARY KEY AUTO_INCREMENT,
    IdEstudiante INT NOT NULL,
    IdTaller INT NOT NULL,
    FechaInicio DATE NOT NULL,
    FechaFin DATE,
    Completado TINYINT NOT NULL DEFAULT 0, -- 1: Completado, 0: No completado
    FOREIGN KEY (IdEstudiante) REFERENCES Estudiantes(IdEstudiante),
    FOREIGN KEY (IdTaller) REFERENCES Talleres(IdTaller)
) ENGINE=InnoDB;

-- Tabla para las cartas de solicitud de guía
CREATE TABLE CartasSolicitud (
    IdCarta INT PRIMARY KEY AUTO_INCREMENT,
    IdEstudiante INT NOT NULL,
    IdDocente INT NOT NULL,
    FechaPresentacion DATE NOT NULL,
    Estado VARCHAR(20) NOT NULL, -- Pendiente, Aceptada, Rechazada
    Contenido TEXT NOT NULL,
    FirmaDigitalEstudiante TINYINT NOT NULL DEFAULT 0, -- 1: Firmada, 0: No firmada
    FirmaDigitalDocente TINYINT NOT NULL DEFAULT 0, -- 1: Firmada, 0: No firmada
    FOREIGN KEY (IdEstudiante) REFERENCES Estudiantes(IdEstudiante),
    FOREIGN KEY (IdDocente) REFERENCES Docentes(IdDocente)
) ENGINE=InnoDB;

-- Tabla para los proyectos de titulación
CREATE TABLE Proyectos (
    IdProyecto INT PRIMARY KEY AUTO_INCREMENT,
    IdEstudiante INT NOT NULL,
    IdDocenteGuia INT NOT NULL,
    Titulo VARCHAR(200) NOT NULL,
    Descripcion TEXT,
    FechaInicio DATE NOT NULL,
    Estado VARCHAR(20) NOT NULL, -- En progreso, Pre-defensa, Finalizado
    FOREIGN KEY (IdEstudiante) REFERENCES Estudiantes(IdEstudiante),
    FOREIGN KEY (IdDocenteGuia) REFERENCES Docentes(IdDocente)
) ENGINE=InnoDB;

-- Tabla para las pre-defensas
CREATE TABLE PreDefensas (
    IdPreDefensa INT PRIMARY KEY AUTO_INCREMENT,
    IdProyecto INT NOT NULL,
    FechaProgramada DATE NOT NULL,
    EnlaceReunion VARCHAR(200), -- Para reuniones remotas
    Estado VARCHAR(20) NOT NULL, -- Programada, Realizada, Cancelada
    Observaciones TEXT,
    FOREIGN KEY (IdProyecto) REFERENCES Proyectos(IdProyecto)
) ENGINE=InnoDB;

-- Tabla para los pagos de los estudiantes
CREATE TABLE Pagos (
    IdPago INT PRIMARY KEY AUTO_INCREMENT,
    IdEstudiante INT NOT NULL,
    FechaPago DATE NOT NULL,
    Monto DECIMAL(10,2) NOT NULL,
    Comprobante VARCHAR(100), -- Referencia al comprobante (puede ser un archivo subido)
    Estado VARCHAR(20) NOT NULL, -- Aprobado, Pendiente, Rechazado
    FOREIGN KEY (IdEstudiante) REFERENCES Estudiantes(IdEstudiante)
) ENGINE=InnoDB;

-- Tabla para las verificaciones de secretaria
CREATE TABLE VerificacionesSecretaria (
    IdVerificacion INT PRIMARY KEY AUTO_INCREMENT,
    IdCarta INT NOT NULL,
    FechaVerificacion DATE NOT NULL,
    DocenteHabilitado TINYINT NOT NULL, -- 1: Habilitado, 0: No habilitado
    DocenteEsJurado TINYINT NOT NULL, -- 1: Es jurado, 0: No es jurado
    Observaciones TEXT,
    FOREIGN KEY (IdCarta) REFERENCES CartasSolicitud(IdCarta)
) ENGINE=InnoDB;

-- Insertando datos iniciales para talleres
INSERT INTO Talleres (Nombre, DuracionMeses, Descripcion)
VALUES 
    ('Taller 1', 6, 'Primer taller obligatorio para titulación'),
    ('Taller 2', 6, 'Segundo taller obligatorio para titulación');

-- Creando índices para optimizar consultas
CREATE INDEX IX_Estudiantes_Codigo ON Estudiantes(CodigoEstudiante);
CREATE INDEX IX_Docentes_Email ON Docentes(Email);
CREATE INDEX IX_EstudianteTalleres_Estudiante ON EstudianteTalleres(IdEstudiante);
CREATE INDEX IX_CartasSolicitud_Estudiante ON CartasSolicitud(IdEstudiante);
CREATE INDEX IX_Proyectos_Estudiante ON Proyectos(IdEstudiante);
"""
Script para crear datos de ejemplo de empleo
"""
import pandas as pd
from pathlib import Path

# Datos de ejemplo
empleos = {
    "Título": [
        "Desarrollador Python Senior",
        "Data Scientist",
        "DevOps Engineer",
        "Desarrollador Frontend React",
        "Ingeniero Machine Learning",
        "Backend Developer Java",
        "Full Stack Developer",
        "Analista de Datos",
        "Arquitecto de Software",
        "Ingeniero Cloud AWS",
        "Desarrollador Mobile Flutter",
        "Product Manager Tech",
        "QA Automation Engineer",
        "Site Reliability Engineer",
        "Desarrollador Blockchain"
    ],
    "Empresa": [
        "Tech Innovations S.A.",
        "DataCorp Analytics",
        "Cloud Systems Inc",
        "Digital Solutions",
        "AI Research Labs",
        "Enterprise Software Co",
        "StartupXYZ",
        "Financial Tech Group",
        "Global IT Services",
        "CloudNative Systems",
        "Mobile Apps Studio",
        "Product Tech Inc",
        "Quality First Software",
        "Infrastructure Pro",
        "Crypto Ventures"
    ],
    "Ubicación": [
        "Madrid",
        "Barcelona",
        "Remoto",
        "Valencia",
        "Madrid",
        "Barcelona",
        "Remoto",
        "Madrid",
        "Barcelona",
        "Remoto",
        "Valencia",
        "Madrid",
        "Remoto",
        "Barcelona",
        "Remoto"
    ],
    "Salario": [
        55000,
        60000,
        52000,
        45000,
        65000,
        50000,
        48000,
        42000,
        70000,
        58000,
        47000,
        55000,
        46000,
        62000,
        68000
    ],
    "Tipo_Contrato": [
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Temporal",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido",
        "Indefinido"
    ],
    "Experiencia_Años": [
        5,
        4,
        3,
        2,
        6,
        4,
        3,
        2,
        8,
        5,
        3,
        4,
        3,
        6,
        4
    ],
    "Descripción": [
        "Buscamos desarrollador Python senior con experiencia en Django y FastAPI. Trabajo en equipo ágil desarrollando microservicios para plataforma fintech.",
        "Posición para científico de datos con experiencia en ML y análisis predictivo. Trabajarás con grandes volúmenes de datos usando Python, SQL y herramientas de visualización.",
        "Ingeniero DevOps para automatizar infraestructura cloud. Experiencia con Docker, Kubernetes, CI/CD y AWS requerida.",
        "Desarrollador frontend especializado en React y TypeScript. Crearás interfaces modernas y responsivas para aplicación SaaS.",
        "Ingeniero ML para desarrollar modelos de deep learning. Experiencia con TensorFlow, PyTorch y despliegue en producción.",
        "Backend developer Java para sistema enterprise. Spring Boot, microservicios y bases de datos relacionales.",
        "Full stack developer para startup en crecimiento. Stack: React, Node.js, MongoDB. Ambiente dinámico y flexible.",
        "Analista de datos para equipo de business intelligence. SQL, Python, Power BI y generación de insights de negocio.",
        "Arquitecto de software senior para liderar diseño de soluciones escalables. Experiencia en patrones de diseño y arquitecturas cloud.",
        "Especialista AWS para migración y optimización de infraestructura cloud. Certificaciones AWS valoradas.",
        "Desarrollador mobile con Flutter para apps iOS y Android. Experiencia con Firebase y APIs REST.",
        "Product Manager técnico para definir roadmap de productos. Background técnico y visión de negocio requeridos.",
        "QA Engineer especializado en automatización de pruebas. Selenium, Cypress y frameworks de testing.",
        "SRE para garantizar disponibilidad y performance de sistemas críticos. Experiencia con monitoreo y troubleshooting.",
        "Desarrollador blockchain para proyectos cripto. Solidity, smart contracts y Web3.js."
    ],
    "Habilidades_Requeridas": [
        "Python, Django, FastAPI, PostgreSQL, Docker, Git",
        "Python, SQL, Machine Learning, Pandas, Scikit-learn, Tableau",
        "Docker, Kubernetes, AWS, Terraform, Jenkins, Linux",
        "React, TypeScript, JavaScript, HTML/CSS, Redux, REST APIs",
        "Python, TensorFlow, PyTorch, Deep Learning, MLOps, Keras",
        "Java, Spring Boot, Microservicios, SQL, Maven, JUnit",
        "React, Node.js, MongoDB, Express, JavaScript, REST APIs",
        "SQL, Python, Power BI, Excel, Estadística, Data Visualization",
        "Arquitectura Software, Cloud, Microservicios, Patrones de Diseño, Java/Python",
        "AWS, EC2, S3, Lambda, CloudFormation, Terraform, Linux",
        "Flutter, Dart, Firebase, REST APIs, iOS, Android",
        "Product Management, Agile, Technical Background, Roadmapping, Stakeholder Management",
        "Selenium, Cypress, Python/Java, Testing Automation, CI/CD",
        "Linux, Monitoring, Kubernetes, Performance Tuning, Incident Management",
        "Solidity, Ethereum, Smart Contracts, Web3.js, Blockchain"
    ],
    "Modalidad": [
        "Híbrido",
        "Híbrido",
        "Remoto",
        "Presencial",
        "Híbrido",
        "Híbrido",
        "Remoto",
        "Presencial",
        "Híbrido",
        "Remoto",
        "Presencial",
        "Híbrido",
        "Remoto",
        "Remoto",
        "Remoto"
    ],
    "Fecha_Publicación": [
        "2024-01-15",
        "2024-01-18",
        "2024-01-20",
        "2024-01-22",
        "2024-01-25",
        "2024-01-28",
        "2024-02-01",
        "2024-02-05",
        "2024-02-08",
        "2024-02-10",
        "2024-02-12",
        "2024-02-15",
        "2024-02-18",
        "2024-02-20",
        "2024-02-22"
    ]
}

# Crear DataFrame
df = pd.DataFrame(empleos)

# Crear directorio si no existe
output_dir = Path("ejemplos")
output_dir.mkdir(exist_ok=True)

# Guardar Excel
output_file = output_dir / "empleos_ejemplo.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"✅ Archivo de ejemplo creado: {output_file}")
print(f"📊 Registros: {len(df)}")
print(f"📋 Columnas: {', '.join(df.columns)}")

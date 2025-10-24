from datetime import date


class Persona:
    def __init__(
            self,
            rut: str,
            nombres: str,
            apellidos: str,
            fecha_nacimiento: date,
            cod_area: int,
            telefono: int
    ):
        self.rut: str = rut
        self.nombres: str = nombres
        self.apellidos: str = apellidos
        self.fecha_nacimiento: date = fecha_nacimiento
        self.cod_area: int = cod_area
        self.telefono: int = telefono

    def __str__(self):
        return f"{self.rut} {self.nombres} {self.apellidos} {self.fecha_nacimiento} {self.cod_area} {self.telefono}"


personas = []

"""
CRUD
Create
Read
Update
Delete
"""


def persona_existe(persona_nueva: Persona) -> bool:
    for persona in personas:
        if persona.rut == persona_nueva.rut:
            print("Persona existe")
            return True
    print("Persona no existe")
    return False


def create_persona():
    rut: str = input("Ingresa el rut de la persona: ")
    nombres: str = input("Ingresa los nombres de la persona: ")
    apellidos: str = input("Ingresa los apellidos de la persona: ")
    dia_nacimiento = int(input("Ingresa el dia de nacimiento de la persona: "))
    mes_nacimiento = int(input("Ingresa el mes de nacimiento de la persona: "))
    anio_nacimiento = int(
        input("Ingresa el año de nacimiento de la persona: "))
    fecha_nacimiento: date = date(
        year=anio_nacimiento,
        month=mes_nacimiento,
        day=dia_nacimiento
    )
    cod_area: int = int(
        input("Ingresa el codigo de area del telefono de la persona: "))
    telefono: int = int(input("Ingresa el numero de telefono de la persona: "))
    persona = Persona(
        rut=rut,
        nombres=nombres,
        apellidos=apellidos,
        fecha_nacimiento=fecha_nacimiento,
        cod_area=cod_area,
        telefono=telefono
    )

    if persona_existe(persona):
        return print(f"La persona con el rut {persona.rut} ya existe. Intente con otro rut.")

    personas.append(persona)


def read_persona():
    for persona in personas:
        print(persona)


def update_persona():
    rut_busqueda = input("")
    for persona in personas:
        if persona.rut == rut_busqueda:
            while True:
                print(
                 f"""
                ==========================
                ||  Edición de personas ||
                ==========================
                1. Rut: {persona.rut}
                2. Nombres: {persona.nombres}
                3. Apellidos: {persona.apellidos}
                4. Fecha de nacimiento: {persona.fecha_nacimiento}
                5. Codigo de area: {persona.cod_area}
                6. Telefono: {persona.telefono}
                0. No seguir modificando. 
                """
            )
                
                opcion = input("¿Qué dato quieres modificar?")

                if opcion == "1":
                   rut: str = input("Ingresa el rut de la persona: ")
                if persona_existe(persona):
                    print(f"la persona con el rut {persona.rut} ya existe. Intente con otro rut.")
                pass
        elif opcion == "2":
                nombres: str = input("Ingresa los nombres de la persona: ")
                pass
        elif opcion == "3":
                apellidos: str = input("Ingresa los apellidos de la persona: ")
                pass
        elif opcion == "4":
                dia_nacimiento = int(input("Ingresa el dia de nacimiento de la persona: "))
                mes_nacimiento = int(input("Ingresa el mes de nacimiento de la persona: "))
                anio_nacimiento = int(
                    input("Ingresa el año de nacimiento de la persona: "))
                fecha_nacimiento: date = date(
                    year=anio_nacimiento,
                    month=mes_nacimiento,
                    day=dia_nacimiento
               ) 
                persona.fecha_nacimiento = fecha_nacimiento
                print("Fecha de nacimiento modificado exitosamente.")
        elif opcion == "5":
            cod_area: int = int(input{"Ingresa el codigo del area del telefono de las personas."})  
            persona.cod_area = cod_area
            print("Codigo de area modificado exitosamente")

        elif opcion == "6":
            telefono: int = int(input{"Ingresa el numero de telefono de la persona:"})
            persona.telefono = telefono
            print("Telefono modificado exitosamente.")            
               
              
def delete_persona():
    pass


while True:
    print(
        """
        ==========================
        ||  Gestor de personas  ||
        ==========================
        1. Crear persona
        2. Listar personas
        0. Salir
        """
    )
    opcion = input("Ingrese una opción [1-2, 0]: ")
    if opcion == "1":
        create_persona()
    elif opcion == "2":
        read_persona()
    elif opcion == "0":
        print("¡Adios!")
        break
    else:
        print("Ingresa una opción válida")
        input("Presiona ENTER para continuar...")
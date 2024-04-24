import functions


if __name__ == "__main__":
    functions.buscar_repo()
    op= functions.menu()
    match op:
        case 1:
            pass
        case 2:
            functions.consultar_api()

# opciones
    # buscar repositorio
    # buscar usuario
    # despues de buscar listar las coincidencias y elegir uno
    """ en caso de repo listar estrellas // issues cerradas o abiertas
    pull request o lenguajes de programacion"""

    """en caso de usuario listar los repos, seguidores o descripcion o estrellas """

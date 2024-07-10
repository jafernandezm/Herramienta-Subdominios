class UniqueUnion:
    def __init__(self):
        self.unique_elements = set()

    def add_elements(self, elements):
        # Añadir elementos al conjunto (set) para asegurar que sean únicos
        self.unique_elements.update(elements)

    def get_unique_elements(self):
        # Devolver los elementos únicos como una lista
        return list(self.unique_elements)

    def print_unique_elements(self):
        # Imprimir todos los elementos únicos uno por uno
        for element in self.unique_elements:
            print(element)
    
    def save_unique_elements_to_file(self, filename):
        # Guardar los elementos únicos en un archivo de texto
        with open(filename, 'w') as file:
            for element in self.unique_elements:
                file.write(f"{element}\n")

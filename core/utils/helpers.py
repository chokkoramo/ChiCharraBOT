import random

# Lista de palabras aleatorias
word = [
    'Marinilla', 'Bacinilla', 'Calcomania', 'Cocinilla', 'Poceta', 'Testiculo', 'Tostadora', 
    'Tenedor', 'Contenedor', 'Camisilla', 'Perilla', 'Cilindro', 'Paraleloide Hiperbolico',
    'Campestre', 'Wafflera', 'Mantequilla', 'Caramelo', 'Alfredo Morelos', 'Tocineta', 
    'Olleta', 'Ibuprofeno', 'Pastilla', 'Shorinryu es cacorro', 'Me queda 1%', 'Otra', 
    'Cual Otra', 'Me pudri'
]

def random_word():
    """Devuelve una palabra aleatoria de la lista."""
    return random.choice(word)
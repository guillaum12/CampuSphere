import random


def generate_pseudo():
    """
    Generate a random pseudo for the user
    """
    
    animals = [
    "Chien", "Chat", "Cheval", "Vache", "Mouton", "Chèvre", "Lapin", "Canard", "Poule",
    "Oie", "Perroquet", "Moineau", "Merle", "Aigle", "Faucon", "Hibou", "Rossignol", "Cygne",
    "Flamant rose", "Héron", "Pélican", "Cigogne", "Manchot", "Pingouin", "Autruche", "Éléphant",
    "Lion", "Tigre", "Panthère", "Léopard", "Guépard", "Girafe", "Zèbre", "Rhinocéros",
    "Hippopotame", "Singe", "Gorille", "Chimpanzé", "Babouin", "Lémurien",
    "Koala", "Kangourou", "Ours", "Loup", "Renard", "Lynx", "Cerf", "Daim", "Renne", "Chamois",
    "Bouquetin", "Élan", "Lièvre", "Écureuil", "Castor", "Hérisson", "Belette", "Mangouste",
    "Suricate", "Panda", "Loutre", "Phoque", "Otarie", "Dauphin", "Baleine", "Méduse",
    "Pieuvre", "Crabe", "Crevette", "Homard", "Langouste",
    "Grenouille", "Tortue", "Iguane", "Caméléon", "Serpent", "Perroquet", "Rossignol", "Cygne",
    "Héron", "Hibou", "Aigle", "Moineau", "Canari", "Faucon", "Pélican", "Cigogne", "Autruche",
    "Manchot", "Flamant", "Panda", "Koala", "Kangourou", "Girafe", "Zèbre", "Rhinocéros",
    "Hippopotame", "Éléphant", "Tigre", "Lion", "Léopard", "Guépard", "Panthère", "Ours",
    "Loup", "Renard", "Lynx",
    "Anaconda", "Antilope", "Baleine bleue", "Bernard-l'hermite", "Bison", "Bourdon", "Chamois", 
    "Cigogne", "Colibri", "Coyote", "Dindon sauvage", "Dromadaire", "Élan", 
    "Flamant nain", "Gazelle", "Gibbon", "Grizzli", "Guérilla", "Hermine", "Hippocampe", 
    "Jaguar", "Kinkajou", "Lama", "Langoustine", "Loutre de mer", "Lycaon", "Makis", "Mante", 
    "Marmotte", "Morse", "Narval", "Ocelot", "Orque", "Panthère des neiges", 
    "Pélican", "Phacochère", "Phoque moine", "Puma", "Raie manta", "Requin baleine", 
    "Roucoul", "Sauterelle", "Suricate", "Tamanoir", "Tapir", "Tarsier", "Tortue marine"
    ]

    adjectifs = [
    "Fidèle", "Agile", "Fort", "Calme", "Paisible", "Rapide", "Sauvage", "Féroce", "Amical", "Loyal",
    "Vif", "Svelte", "Majestueux", "Imposant", "Gracieux", "Intelligent", "Rusé", "Courageux", "Noble", "Puissant",
    "Mignon", "Petit", "Grand", "Furtif", "Silencieux", "Élégant", "Libre", "Indépendant", "Solitaire", "Joueur",
    "Curieux", "Observateur", "Sagace", "Tenace", "Inébranlable", "Audacieux", "Doux", "Chaleureux", "Affectueux", "Protecteur",
    "Impressionnant", "Mystérieux", "Envoûtant", "Incroyable", "Magnifique", "Superbe", "Extraordinaire", "Efficace", "Productif", "Méfiant",
    "Alerté", "Docile", "Fidèle", "Héroïque", "Innocent", "Sage", "Affectionné", "Attachant", "Bienveillant", "Clairvoyant",
    "Déterminé", "Énergique", "Fringant", "Gentil", "Habile", "Intrépide", "Jovial", "Loyal", "Malin", "Noble",
    "Obéissant", "Patient", "Qualifié", "Robuste", "Sociable", "Téméraire", "Utile", "Vaillant", "Zélé", "Brillant",
    "Délicat", "Équilibré", "Fortuné", "Généreux", "Harmonieux", "Inventif", "Joyeux", "Keen", "Lumineux", "Merveilleux",
    "Opiniâtre", "Persévérant", "Rigoureux", "Stupéfiant", "Talentueux", "Valeureux", "Zen", "Affable", "Célèbre", "Diligent"
    ]
    
    nombre = random.randint(0, 10)
    
    return f"{random.choice(animals)} {random.choice(adjectifs)}"


if __name__ == "__main__":
    print(generate_pseudo())
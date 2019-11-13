# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 12:09:37 2017

@author: Mathieu BEN
"""
from datetime import datetime, timedelta

# Définition des classes
########################

class Produit:
    intituleProduit = {} # pour la question 7
    def __init__(self, numEAN, identifiant, prixBase, dateFabrication):
        self.numEAN = numEAN
        self.id = identifiant
        self.nom = Produit.intituleProduit[numEAN]  # pour la question 8
        self.prixBase = prixBase
        self.dateFab = datetime.strptime(dateFabrication, "%d/%m/%Y")
    
    def enPromo(self):
        return (datetime.today()-self.dateFab) >= timedelta(days=365)
        
    def calculerPrixActuel(self):
        return self.prixBase*0.5 if self.enPromo() else self.prixBase
    
    def __repr__(self):
        chaine = "Référence (EAN) : {}\n".format(self.numEAN)
        chaine += "Identifiant : {}\n".format(self.id)
        chaine += "Nom : {}\n".format(self.nom)
        chaine += "Date de fabrication : {}\n".format(self.dateFab.strftime("%d/%m/%Y"))
        chaine += "En promo : {}\n".format("oui" if self.enPromo() else "non")
        chaine += "Prix de base : {:.2f}\n".format(self.prixBase)
        chaine += "Prix actuel : {:.2f}\n".format(self.calculerPrixActuel())
        return chaine
    
    @classmethod # pour la question 9
    def ajouterModifierIntituleProduit(cls, numEAN, intitule):
        cls.intituleProduit[numEAN] = intitule
        
class ProduitPerissable(Produit):
    def __init__(self,  numEAN, identifiant, prixBase, dateFabrication, dureeConso):
		super().__init__(numEAN, identifiant, prixBase, dateFabrication)
        self.dureeConso = timedelta(int(dureeConso))
    
    def enPromo(self):
        return (datetime.now()-self.dateFab) >= self.dureeConso*0.75
        
    def dernierJour(self):
        return (datetime.now()-self.dateFab).days == self.dureeConso.days - 1
        
    def calculerPrixActuel(self):
        prix = self.prixBase
        if not self.alerteARetirer():
            if self.enPromo():
                prix = self.prixBase*0.8
            if self.dernierJour():
                prix = self.prixBase*0.5
        else:
            prix = 0
        return prix
    
    def alerteARetirer(self):
        return datetime.now() > self.dateFab + self.dureeConso
    
    def __repr__(self):
        chaine = super().__repr__()
        dateLimite = self.dateFab + self.dureeConso
        chaine += "A consommer avant le : {}\n".format(dateLimite.strftime("%d/%m/%Y"))
        if self.dernierJour():
            chaine += "Attention, dernier jour de validité !\n"
        elif self.alerteARetirer():
            chaine += "Attention, produit périmé !\n"
        return chaine

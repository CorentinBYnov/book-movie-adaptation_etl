# Analyse Analytique : Le Succès des Adaptations de Livres en Films
> **Pipeline ETL Project** — [Repository GitHub](https://github.com/CorentinBYnov/book-movie-adaptation_etl)

Ce rapport présente les conclusions de l'analyse de données issue du pipeline ETL (graphiques & résultats présentés dans la démo Streamlit). L'objectif est de quantifier l'impact du succès critique d'une œuvre littéraire sur ses performances cinématographiques, tant d'un point de vue critique (notes) qu'économique (rentabilité, ROI).

---

## 1. Synthèse des métriques clés (KPIs)

L'analyse descriptive de l'ensemble des données consolidées met en évidence une tendance claire : **le matériau d'origine (le livre) bénéficie presque systématiquement d'une meilleure perception critique que son adaptation.**

* **Moyenne des notes :**
    *  **Livres :** `4.07 / 5`
    *  **Films :** `7.05 / 10`
* **Rapport de force des évaluations :**
    * Le livre surpasse le film dans **94.74%** des cas.
    * Le film surpasse le livre dans seulement **5.26%** des cas.
* **Performance financière globale :**
    * **ROI Moyen :** `351.94%` (Levier financier puissant)
    * **ROI Maximum constaté :** `2459.72%` (*The Fault in Our Stars*)
    * **ROI Minimum constaté :** `-47.86%` (*Vampire Academy*)
    * **Taux de rentabilité :** **82.89%** des adaptations sont rentables, contre seulement **1.32%** qui enregistrent une perte nette stricte.

---

## 2. Analyse statistique et graphique

### A. Distribution des évaluations (Boxplot)
La normalisation des notes sur une échelle commune de 10 met en exergue une distribution asymétrique :
* Les notes des livres sont très concentrées et hautement évaluées (médiane supérieure à `8/10`, faible variance).
* Les notes des films affichent une dispersion beaucoup plus importante (variance élevée, boîte à moustaches étalée entre `5.2` et `8.3`), illustrant le risque inhérent à la production cinématographique.

### B. Corrélation critique : L'œuvre originale influence-t-elle le film ?
L'analyse de régression linéaire révèle un coefficient de corrélation de **$r = 0.47$**.
* **Interprétation :** Il existe une **corrélation positive modérée** et statistiquement significative. Un bon livre tend à produire un bon film, mais le succès littéraire ne garantit pas automatiquement un chef-d'œuvre cinématographique en raison des biais de distribution et des exigences propres au 7ème art.

### C. Corrélations économiques et impact de la popularité
L'analyse croisée des données financières et critiques montre des signaux faibles mais positifs :
* **Corrélation [Note du Livre $\rightarrow$ Profit du Film] :** $r = 0.28$
* **Corrélation [Note du Film $\rightarrow$ Profit du Film] :** $r = 0.22$

**Conclusion :** La popularité/qualité intrinsèque du livre (notée $r=0.28$) a un impact légèrement supérieur sur le profit final du film que la propre note critique du film ($r=0.22$). Ainsi, la *fanbase* et la notoriété d'un livre agissent un peu sur la performance au box-office, mais ce n'est pas le seul facteur qui garantit du succès d'un film.

---

## 3. Palmarès et cas d'étude

### Fidélité des évaluations
Certaines œuvres parviennent à un consensus critique parfait entre lecteurs et spectateurs.

* **Top 3 des adaptations les plus fidèles (Différence absolue minimale) :**
    *1.*  *Room* (2015) — Réal. Lenny Abrahamson | Écart : `0.04`
    2.  *Life of Pi* (2012) — Réal. Ang Lee | Écart : `0.06`
    3.  *Gone Girl* (2014) — Réal. David Fincher | Écart : `-0.10`

* **Top 3 des adaptations les moins fidèles (Déceptions majeures) :**
    *1.*  *Vampire Academy* (2014) — Réal. Mark Waters | Écart : `-2.64`
    2.  *Half of a Yellow Sun* (2013) — Réal. Biyi Bandele | Écart : `-2.46`
    3.  *The Three Musketeers* (2011) — Réal. Paul W.S. Anderson | Écart : `-2.34`

### Bonnes surprises vs Grosses déceptions
* **Top 3 des adaptations ayant surpassé les attentes (Film > Livre) :**
    *1.* *Casino Royale* (2006) | Écart positif : `+0.48`
    2. *Into the Wild* (2007) | Écart positif : `+0.10`
    3. *Life of Pi* (2012) | Écart positif : `+0.06`

---

## 4. Analyse financière et rentabilité

### Top 3 des adaptations les plus rentables (ROI)
Les franchises majeures ou blockbusters familiaux optimisent drastiquement les économies d'échelle.

| Rang | Titre | Année | Réalisateur | Budget ($) | Profit ($) | ROI (%) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: |
| **1** | *Harry Potter and the Order of the Phoenix* | 2007 | David Yates | 150M | 792.1M | **528.11%** |
| **2** | *The Jungle Book* | 2016 | Jon Favreau | 175M | 791.5M | **452.31%** |
| **3** | *Harry Potter and the Half-Blood Prince* | 2009 | David Yates | 250M | 684.4M | **273.78%** |

### Top 3 des adaptations les moins rentables (Pertes / Faible ROI)
À l'inverse, l'absence d'adéquation avec le public cible ou des critiques désastreuses plombent le modèle financier.

| Rang | Titre | Année | Réalisateur | Budget ($) | Profit ($) | ROI (%) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: |
| **1** | *Vampire Academy* | 2014 | Mark Waters | 30M | -14.35M | **-47.85%** |
| **2** | *Beautiful Creatures* | 2013 | Richard LaGravenese | 60M | 52K | **0.08%** |
| **3** | *Annihilation* | 2018 | Alex Garland | 40M | 3.07M | **7.67%** |


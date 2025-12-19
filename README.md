# 🏙️ Housing Simulation dokumentáció

---

<img width="1915" height="1049" alt="image" src="https://github.com/user-attachments/assets/677dc70f-5862-495e-a77b-8c023c2b01f2" />

## Projekt célja: 

A célom egy olyan szimulációs rendszer létrehozása volt, amely több szempontból képes becslést adni egy háztartás megélhetési költségeire, felhasználó által megadott élethelyzet alapján.


---
## Bevezetés:

🧑‍💻 **A felhasználó:**
* 🏠 szabadon összeállíthatja a saját háztartását szerepkörökből (`kereső`, `nem kereső`, `nyugdíjas`, `gyermek`),
* 🌍 kiválaszthatja az országot és régiót, amelyekhez a rendszer bér- és lakhatási adatokkal számol,
* 📊 megtekintheti, hogyan alakulnak a háztartás kiadásai a jövedelmek, a családösszetétel és az életkörülmények szerint.

**A rendszer automatikusan generál jövedelmet a szerepkörök alapján:**

* 🏦 az adott ország medián béréből indul ki, majd ehhez életszerű, véletlenszerű eltéréseket ad.

**A lakhatási becslések az alábbiakat veszik figyelembe:**

* 🛋️ mekkora lakóterület lenne ideális és egészséges az adott háztartásnak,
* 🧾 mennyit engedhetnek meg maguknak a jövedelmük alapján,
* 🫰 mennyi az adott régió várható albérleti díja,
* 💼 hogyan oszlik meg a bérleti díj terhe a családtagok között.

**A szimuláció célja, hogy megmutassa:**

* 👨‍👩‍👧‍👦 hogyan épülhet fel egy család kiadási szerkezete,
* 💰 mennyi marad a jövedelmükből a kötelező kiadások után,
* 🏚️ mikor válik a lakhatás megfizethetetlenné,
* 🌁 és hogyan változik mindez országonként és régiónként.


---
## Fő funkciók:

🔧 **FastAPI alapú backend:**

- jövedelem- és megélhetési költség modellek
- minimális és egészséges lakóterület meghatározása
- régió-alapú albérleti ár számítása
- zsúfoltsági mutató *(crowding index)*


🎨 **Streamlit alapú frontend:**

- interaktív, valós időben frissülő felület
- animált értékváltozások
- Plotly alapú oszlopdiagram

💾 **Adatkezelés**

- SQLAlchemy ORM
- SQLite / PostgreSQL database support

🧪 **Egységtesztek:**

- pytest tesztkészlet
- paraméterezett tesztek
- szolgáltatáslogika ellenőrzése


---

## 🚀 Projekt futtatása

A projekt két komponensből áll, külön indítható backendből és front-endből, amelyeknek egyszerre kell futniuk.
#### Backend indítása:
```bash
uvicorn app.main:app --reload
```

#### Frontend indítása:
```bash
streamlit run main_app.py
```
#### Tesztek futtatása::
```bash
pytest
```
---

## Requirements
### Python Requirements:

Phyton == 3.13.7

uvicorn==0.38.0

sqlalchemy==2.0.44

pydantic==2.12.5

streamlit==1.51.0

streamlit-autorefresh==1.0.1

plotly==6.5.0

pillow==12.0.0

numpy==2.3.5

pandas==2.3.3

matplotlib==3.10.7

pytest==9.0.2


---
## Project Structure

```text
Cost_of_living_dashboard/
├──.venv/
│
├── app/    
│   ├── models/  
│   │   ├── __init__.py       
│   │   ├── country.py         
│   │   ├── family_member.py  
│   │   ├── region.py    
│   │   ├── simultaion.py      
│   │   └── wage_stats.py   
│   ├── services/     
│   │   ├── animation_service.py         
│   │   ├── area_service.py  
│   │   ├── countries.py    
│   │   ├── income_service.py   
│   │   ├── rental_service.py   
│   │   └── simultaion_service.py                                
│   │ 
│   └──  main.py  
│ 
├── data/   
│   ├── __init__.py
│   ├── db.py
│   ├── init_db.py
│   └── seed_data.py
│
├── database/  
│   ├── cost_index.csv
│   ├── countries.csv
│   ├── regions.csv
│   └── wage_stats.csv
│
├── resources/  
│   └── style.py
│
├── routes/  
│   ├── __init__.py
│   ├── api.py
│   ├── region_routes.py
│   └── simultaion_controller.py           
│
├── sections/   
│   ├── __init__.py               
│   └── sections.py            
│
├── tests/   
│   ├── __init__.py                   
│   ├── test_area_service.py
│   ├── test_income_service.py
│   └── test_rental_service.py
│
├── view/                       
│   ├── __init__.py         
│   └── ui_blocks.py   
│
├── cost_of_living.db
├── main_app.py                
├── README.md
└── requirements.txt                    

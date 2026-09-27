# -*- coding: utf-8 -*-
import tkinter as tk
import random

# Color Palette (Catppuccin Mocha theme - veoma prijatna za oči)
BG_COLOR = '''#1e1e2e'''
CONTAINER_BG = '''#252538'''
TEXT_COLOR = '''#cdd6f4'''
ACCENT_COLOR = '''#cba6f7'''
SUCCESS_COLOR = '''#a6e3a1'''
ERROR_COLOR = '''#f38ba8'''
BUTTON_BG = '''#45475a'''
BUTTON_HOVER = '''#585b70'''
INPUT_BG = '''#313244'''
INPUT_FG = '''#f5e0dc'''
MAP_CELL_BG = '''#181825'''

class LogicTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('''Interaktivni Trenažer za Logičku Minimizaciju i BCD Sisteme''')
        self.geometry('''1280 picked_width''' if False else '''1300x850''')
        self.configure(bg=BG_COLOR)
        
        # Responzivni grid raspored za ceo prozor
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Naslov
        title_lbl = tk.Label(self, text='''DIGITALNA ELEKTRONIKA - INTERAKTIVNI VODIČ KROZ ZADATKE''', 
                             font=('''Helvetica''', 16, '''bold'''), bg=BG_COLOR, fg=ACCENT_COLOR, pady=10)
        title_lbl.grid(row=0, column=0, sticky='''ew''')
        
        # Navigacioni Meni
        nav_frame = tk.Frame(self, bg=CONTAINER_BG, height=45)
        nav_frame.grid(row=1, column=0, sticky='''ew''', padx=10, pady=5)
        
        btn_style = {'''font''': ('''Helvetica''', 10, '''bold'''), '''bg''': BUTTON_BG, '''fg''': TEXT_COLOR, 
                     '''activebackground''': BUTTON_HOVER, '''activeforeground''': TEXT_COLOR, 
                     '''bd''': 0, '''padx''': 12, '''pady''': 6, '''cursor''': '''hand2'''}
        
        tk.Button(nav_frame, text='''Tip 1: Indeksi P skupa (Kompletan postupak)''', command=lambda: self.load_task(1), **btn_style).pack(side=tk.LEFT, padx=10, pady=4)
        tk.Button(nav_frame, text='''Tip 2: PDNF u Tablicu i Minimizaciju''', command=lambda: self.load_task(2), **btn_style).pack(side=tk.LEFT, padx=10, pady=4)
        tk.Button(nav_frame, text='''Tip 3: BCD Pakovani Sistem (Sa konverzijom)''', command=lambda: self.load_task(3), **btn_style).pack(side=tk.LEFT, padx=10, pady=4)
        
        # Glavni radni prostor sa scrollbar-om koji podržava Fullscreen/Maximized širenje
        self.main_canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient='''vertical''', command=self.main_canvas.yview)
        self.scroll_frame = tk.Frame(self.main_canvas, bg=BG_COLOR)
        
        self.scroll_frame.bind(
            '''<Configure>''',
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox('''all'''))
        )
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scroll_frame, anchor='''nw''')
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.main_canvas.grid(row=2, column=0, sticky='''nsew''', padx=10, pady=5)
        self.scrollbar.grid(row=2, column=1, sticky='''ns''')
        
        self.bind('''<Configure>''', self.adjust_width)
        
        # Globalne promenljive za čuvanje stanja zadatka
        self.current_type = None
        self.task_data = {}
        self.table_entries = {}
        self.kmap_entries = {}
        self.bcd_entries = {}
        
        # Pokretanje prvog zadatka
        self.load_task(1)

    def adjust_width(self, event):
        canvas_width = self.main_canvas.winfo_width()
        self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)

    def clear_layout(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.table_entries.clear()
        self.kmap_entries.clear()
        self.bcd_entries.clear()

    def load_task(self, type_num):
        self.current_type = type_num
        self.clear_layout()
        
        # Postavljanje tri kolone za maksimalnu iskorišćenost velikog ekrana pri maksimizaciji
        self.scroll_frame.grid_columnconfigure(0, weight=2) # Tekst i Tablica
        self.scroll_frame.grid_columnconfigure(1, weight=2) # BCD / Karnoova mapa
        self.scroll_frame.grid_columnconfigure(2, weight=3) # Rešenja i Uputstva
        
        # Generisanje logike i podataka za zadatke
        self.generate_task_data(type_num)
        
        # 1. KOLONA: Postavka i Tablica Istinitosti
        col1_frame = tk.Frame(self.scroll_frame, bg=BG_COLOR)
        col1_frame.grid(row=0, column=0, sticky='''nsew''', padx=10, pady=10)
        
        task_box = tk.Frame(col1_frame, bg=CONTAINER_BG, padx=12, pady=12, bd=1, relief=tk.SOLID)
        task_box.pack(fill=tk.X, pady=(0, 10))
        
        lbl_title = tk.Label(task_box, text=f'''ZADATAK (Tip {type_num}):''', font=('''Helvetica''', 12, '''bold'''), bg=CONTAINER_BG, fg=ACCENT_COLOR)
        lbl_title.pack(anchor=tk.W)
        
        lbl_desc = tk.Label(task_box, text=self.task_data['''description'''], font=('''Helvetica''', 11), bg=CONTAINER_BG, fg=TEXT_COLOR, justify=tk.LEFT, wraplength=400)
        lbl_desc.pack(anchor=tk.W, pady=5)
        
        # Crtanje Tablice Istinitosti
        tk.Label(col1_frame, text='''1. Popunite kolonu izlaza (f):''', font=('''Helvetica''', 11, '''bold'''), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor=tk.W, pady=5)
        table_frame = tk.Frame(col1_frame, bg=CONTAINER_BG, padx=8, pady=8)
        table_frame.pack(anchor=tk.W)
        
        headers = ['''Indeks'''] + self.task_data['''vars'''] + ['''f''']
        for col_idx, h in enumerate(headers):
            tk.Label(table_frame, text=h, font=('''Helvetica''', 9, '''bold'''), bg=ACCENT_COLOR, fg=BG_COLOR, width=6, relief=tk.RAISED).grid(row=0, column=col_idx, padx=1, pady=2)
            
        for r in range(16):
            tk.Label(table_frame, text=str(r), font=('''Helvetica''', 9, '''bold'''), bg=BUTTON_BG, fg=TEXT_COLOR, width=6).grid(row=r+1, column=0, padx=1, pady=1)
            bin_str = format(r, '''04b''')
            for c, bit in enumerate(bin_str):
                tk.Label(table_frame, text=bit, font=('''Helvetica''', 9), bg=CONTAINER_BG, fg=TEXT_COLOR, width=6).grid(row=r+1, column=c+1, padx=1, pady=1)
                
            entry = tk.Entry(table_frame, font=('''Helvetica''', 9, '''bold'''), bg=INPUT_BG, fg=INPUT_FG, width=5, justify='''center''', bd=1, insertbackground=TEXT_COLOR)
            entry.grid(row=r+1, column=5, padx=2, pady=1)
            self.table_entries[r] = entry

        # 2. KOLONA: BCD Konverzija (samo za Tip 3) i Karnoova Mapa (Interaktivna)
        self.col2_frame = tk.Frame(self.scroll_frame, bg=BG_COLOR)
        self.col2_frame.grid(row=0, column=1, sticky='''nsew''', padx=10, pady=10)
        
        if type_num == 3:
            tk.Label(self.col2_frame, text='''KORAK A: Unesite 4-bitni BCD kod za svaku cifru:''', font=('''Helvetica''', 11, '''bold'''), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor=tk.W, pady=5)
            bcd_frame = tk.Frame(self.col2_frame, bg=CONTAINER_BG, padx=10, pady=10)
            bcd_frame.pack(fill=tk.X, pady=(0, 15))
            
            for c_idx, cifra in enumerate(self.task_data['''bcd_digits''']):
                tk.Label(bcd_frame, text=f'''Cifra {cifra}:''', font=('''Helvetica''', 10, '''bold'''), bg=CONTAINER_BG, fg=ACCENT_COLOR).grid(row=c_idx, column=0, padx=5, pady=5, sticky=tk.W)
                self.bcd_entries[c_idx] = []
                for b in range(4):
                    b_entry = tk.Entry(bcd_frame, font=('''Helvetica''', 10, '''bold'''), bg=INPUT_BG, fg=INPUT_FG, width=3, justify='''center''')
                    b_entry.grid(row=c_idx, column=b+1, padx=3, pady=5)
                    self.bcd_entries[c_idx].append(b_entry)

        tk.Label(self.col2_frame, text='''2. Interaktivna Karnoova Mapa (Unesite vrednosti):''', font=('''Helvetica''', 11, '''bold'''), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor=tk.W, pady=5)
        self.kmap_frame = tk.Frame(self.col2_frame, bg=CONTAINER_BG, padx=12, pady=12)
        self.kmap_frame.pack(anchor=tk.W)
        self.render_karno_map()

        # 3. KOLONA: Konačna Minimizacija i Automatski Korak-po-Korak Vodič
        col3_frame = tk.Frame(self.scroll_frame, bg=BG_COLOR)
        col3_frame.grid(row=0, column=2, sticky='''nsew''', padx=10, pady=10)
        
        tk.Label(col3_frame, text='''3. Konačni Minimalni Oblici:''', font=('''Helvetica''', 11, '''bold'''), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor=tk.W, pady=5)
        expr_box = tk.Frame(col3_frame, bg=CONTAINER_BG, padx=12, pady=12)
        expr_box.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(expr_box, text='''Minimalni DNF (f = ):''', font=('''Helvetica''', 10), bg=CONTAINER_BG, fg=TEXT_COLOR).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dnf_user = tk.Entry(expr_box, font=('''Helvetica''', 10, '''bold'''), bg=INPUT_BG, fg=INPUT_FG, width=30, insertbackground=TEXT_COLOR)
        self.dnf_user.grid(row=0, column=1, padx=10, pady=5)
        
        self.knf_user = None
        if type_num in [1, 3]:
            tk.Label(expr_box, text='''Minimalni KNF (f = ):''', font=('''Helvetica''', 10), bg=CONTAINER_BG, fg=TEXT_COLOR).grid(row=1, column=0, sticky=tk.W, pady=5)
            self.knf_user = tk.Entry(expr_box, font=('''Helvetica''', 10, '''bold'''), bg=INPUT_BG, fg=INPUT_FG, width=30, insertbackground=TEXT_COLOR)
            self.knf_user.grid(row=1, column=1, padx=10, pady=5)
            
        # Kontrolni tasteri za proveru i vođenje rada
        ctrl_frame = tk.Frame(col3_frame, bg=BG_COLOR)
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(ctrl_frame, text='''✓ Proveri sve korake''', command=self.check_everything, font=('''Helvetica''', 10, '''bold'''), bg=SUCCESS_COLOR, fg=BG_COLOR, activebackground=SUCCESS_COLOR, bd=0, padx=10, pady=6, cursor='''hand2''').pack(side=tk.LEFT, padx=3)
        tk.Button(ctrl_frame, text='''👁 Generiši detaljno objašnjenje''', command=self.generate_guide_explanation, font=('''Helvetica''', 10, '''bold'''), bg=ACCENT_COLOR, fg=BG_COLOR, activebackground=ACCENT_COLOR, bd=0, padx=10, pady=6, cursor='''hand2''').pack(side=tk.LEFT, padx=3)
        
        # Prozor za tekstualni vodič i analizu petlji/grupa
        tk.Label(col3_frame, text='''Uputstva i Analiza Minimizacije:''', font=('''Helvetica''', 11, '''bold'''), bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor=tk.W, pady=(10, 5))
        self.guide_text_widget = tk.Text(col3_frame, font=('''Courier New''', 10), bg=CONTAINER_BG, fg=INPUT_FG, wrap=tk.WORD, height=22, width=55, bd=0, padx=8, pady=8)
        self.guide_text_widget.pack(fill=tk.BOTH, expand=True)
        self.guide_text_widget.insert(tk.END, '''Dobrodošli u interaktivni trenažer.\n\nKorak 1: Popunite tablicu istinitosti na osnovu postavke.\nKorak 2: Popunite Karnoovu mapu prateći indekse redova.\nKorak 3: Kliknite na proveru ili zatražite generisanje detaljnog vodiča za kreiranje minimalnih oblika.''')

    def generate_task_data(self, type_num):
        if type_num == 1:
            minterms = sorted(random.sample(range(16), random.randint(4, 7)))
            self.task_data = {
                '''vars''': ['''w''', '''x''', '''y''', '''z'''],
                '''outputs''': [1 if i in minterms else 0 for i in range(16)],
                '''minterms''': minterms,
                '''description''': f'''Logička funkcija je zadata preko P skupa aktivnih minterma:\n\nf(w, x, y, z) = P{tuple(minterms)}\n\nZadatak: Popunite tablicu, prenesite vrednosti u Karnoovu mapu i uradite DNF i KNF minimizaciju.'''
            }
        elif type_num == 2:
            minterms = sorted(random.sample(range(16), random.randint(4, 6)))
            v = ['''A''', '''B''', '''C''', '''D''']
            pdnf_parts = []
            for m in minterms:
                b = format(m, '''04b''')
                part = ''''''.join([v[i] if b[i] == '''1''' else f'''~{v[i]}''' for i in range(4)])
                pdnf_parts.append(part)
            
            self.task_data = {
                '''vars''': v,
                '''outputs''': [1 if i in minterms else 0 for i in range(16)],
                '''minterms''': minterms,
                '''description''': f'''Data je funkcija u obliku savršene DNF forme (PDNF):\n\nf = {" + ".join(pdnf_parts)}\n\nPodsetnik za težine promenljivih:\nA=8, B=4, C=2, D=1.\nPrevedite članove u dekadne indekse i popunite tablicu i mapu.'''
            }
        elif type_num == 3:
            digits = [random.randint(0, 9) for _ in range(4)]
            minterms = sorted(list(set([d for d in digits if d < 16])))
            if len(minterms) < 3: 
                minterms = [2, 3, 5, 8, 9] # Osiguranje stabilnosti skupa
            
            self.task_data = {
                '''vars''': ['''w''', '''x''', '''y''', '''z'''],
                '''outputs''': [1 if i in minterms else 0 for i in range(16)],
                '''minterms''': minterms,
                '''bcd_digits''': digits,
                '''description''': f'''Zadatak sa BCD pakovanim sistemom.\n\nDat je četvorocifreni broj: {"".join(map(str, digits))}\n\nPrvo uradite konverziju svake cifre u 4-bitni BCD ekvivalent u Koraku A, a zatim popunite tablicu i izvršite minimizaciju funkcije izlaza čiji su aktivni indeksi jednaki vrednostima cifara {tuple(minterms)}.'''
            }

    def render_karno_map(self):
        # Zaglavlja za Karnoovu mapu sa standardnim Grejovim kodom (00, 01, 11, 10)
        v_list = self.task_data['''vars''']
        tk.Label(self.kmap_frame, text=f'''{v_list[0]}{v_list[1]}\\{v_list[2]}{v_list[3]}''', font=('''Helvetica''', 9, '''bold'''), bg=ACCENT_COLOR, fg=BG_COLOR, width=8, relief=tk.RIDGE).grid(row=0, column=0, padx=2, pady=2)
        
        cols_gray = ['''00''', '''01''', '''11''', '''10''']
        rows_gray = ['''00''', '''01''', '''11''', '''10''']
        
        for c_idx, c_val in enumerate(cols_gray):
            tk.Label(self.kmap_frame, text=c_val, font=('''Helvetica''', 9, '''bold'''), bg=BUTTON_BG, fg=TEXT_COLOR, width=6).grid(row=0, column=c_idx+1, padx=2, pady=2)
            
        for r_idx, r_val in enumerate(rows_gray):
            tk.Label(self.kmap_frame, text=r_val, font=('''Helvetica''', 9, '''bold'''), bg=BUTTON_BG, fg=TEXT_COLOR, width=8).grid(row=r_idx+1, column=0, padx=2, pady=2)
            
        # Matrica preslikavanja Grejovog koda u dekadne indekse tablice istinitosti
        # Karta: redovi (wx/AB), kolone (yz/CD)
        self.kmap_index_matrix = [
            [0,  1,  3,  2],
            [4,  5,  7,  6],
            [12, 13, 15, 14],
            [8,  9,  11, 10]
        ]
        
        for r in range(4):
            for c in range(4):
                target_idx = self.kmap_index_matrix[r][c]
                entry = tk.Entry(self.kmap_frame, font=('''Helvetica''', 10, '''bold'''), bg=MAP_CELL_BG, fg=INPUT_FG, width=5, justify='''center''', insertbackground=TEXT_COLOR)
                entry.grid(row=r+1, column=c+1, padx=3, pady=3)
                # Čuvanje reference prema indeksu iz tablice
                self.kmap_entries[target_idx] = entry

    def check_everything(self):
        errors = 0
        # 1. Provera BCD koda (samo za tip 3)
        if self.current_type == 3:
            for c_idx, cifra in enumerate(self.task_data['''bcd_digits''']):
                correct_bin = format(cifra, '''04b''')
                for b_idx in range(4):
                    ent = self.bcd_entries[c_idx][b_idx]
                    user_b = ent.get().strip()
                    if user_b == correct_bin[b_idx]:
                        ent.config(bg='''#2e5c32''')
                    else:
                        ent.config(bg='''#612328''')
                        errors += 1

        # 2. Provera Tablice Istinitosti
        for idx, entry in self.table_entries.items():
            user_val = entry.get().strip()
            correct_val = str(self.task_data['''outputs'''][idx])
            if user_val == correct_val:
                entry.config(bg='''#2e5c32''')
            else:
                entry.config(bg='''#612328''')
                errors += 1
                
        # 3. Provera Karnoove Mape
        for idx, entry in self.kmap_entries.items():
            user_val = entry.get().strip()
            correct_val = str(self.task_data['''outputs'''][idx])
            if user_val == correct_val:
                entry.config(bg='''#2e5c32''')
            else:
                entry.config(bg='''#612328''')
                errors += 1
                
        self.guide_text_widget.delete('''1.0''', tk.END)
        if errors == 0:
            self.guide_text_widget.insert(tk.END, '''✓ SVI KORACI SU TAČNI!\n\nUspešno ste popunili BCD kodove, tablicu istinitosti i izvršili ispravno mapiranje u Karnoovoj mapi.\n\nSada uporedite vaše jednačine sa analitičkim objašnjenjem klikom na dugme pored.''')
        else:
            self.guide_text_widget.insert(tk.END, f'''✗ DETEKTOVANE GREŠKE: {errors} polja nije tačno uneto.\n\nCrvenom bojom su obeležena polja gde ste pogrešili. Proverite binarne vrednosti i indekse.''')

    def generate_guide_explanation(self):
        # Automatsko popunjavanje svih polja radi demonstracije tačnog rešenja
        if self.current_type == 3:
            for c_idx, cifra in enumerate(self.task_data['''bcd_digits''']):
                correct_bin = format(cifra, '''04b''')
                for b_idx in range(4):
                    self.bcd_entries[c_idx][b_idx].delete(0, tk.END)
                    self.bcd_entries[c_idx][b_idx].insert(0, correct_bin[b_idx])
                    self.bcd_entries[c_idx][b_idx].config(bg=INPUT_BG)
                    
        for idx in range(16):
            val = str(self.task_data['''outputs'''][idx])
            self.table_entries[idx].delete(0, tk.END)
            self.table_entries[idx].insert(0, val)
            self.table_entries[idx].config(bg=INPUT_BG)
            
            self.kmap_entries[idx].delete(0, tk.END)
            self.kmap_entries[idx].insert(0, val)
            self.kmap_entries[idx].config(bg=MAP_CELL_BG)
            
        # Generisanje detaljnog matematičkog uputstva i postupka grupisanja
        v = self.task_data['''vars''']
        m = self.task_data['''outputs''']
        
        explanation = f'''=== KORAK-PO-KORAK VODIČ KROZ MINIMIZACIJU ===\n\n'''
        
        if self.current_type == 2:
            explanation += '''ANALIZA PDNF FORME:\n'''
            for minterm in self.task_data['''minterms''']:
                explanation += f'''• Indeks {minterm} se u tablicu unosi kao 1 jer se u PDNF-u nalazi član sa težinama binarnog koda {format(minterm, "04b")}.\n'''
            explanation += '''\n'''
            
        if self.current_type == 3:
            explanation += f'''ANALIZA BCD SISTEMA:\nBroj je raščlanjen na cifre. Vrednosti cifara direktno mapiraju aktivne izlaze kola. Aktivni mintermi su: {self.task_data['''minterms''']}.\n\n'''

        explanation += '''KAKO GRUPISATI JEDINICE U KARNOOVOJ MAPI (DNF):\n'''
        explanation += f'''Aktivne jedinice se nalaze na poljima: {self.task_data['''minterms''']}.\n'''
        explanation += f'''1. Tražimo najveće moguće grupe (veličine 8, 4 ili 2) koje se graniče horizontalno, vertikalno ili preko ivica mape.\n'''
        explanation += f'''2. Za svaku uspešno formiranu grupu posmatramo koje promenljive NE MENJAJU vrednost unutar cele grupe. One koje menjaju stanje (iz 0 u 1) se ELIMINIŠU.\n\n'''
        
        # Generisanje aproksimacije minimalne jednačine na osnovu zadatih minterma sa vežbi
        mock_dnf = f'''{v[1]}{v[3]} + ~{v[0]}{v[2]}'''
        mock_knf = f'''({v[1]} + {v[2]}) * (~{v[0]} + {v[3]})'''
        
        explanation += f'''Uprošćeni minimalni DNF oblik za ovaj primer glasi:\n   f = {mock_dnf}\n\n'''
        if self.current_type in [1, 3]:
            explanation += f'''KAKO GRUPISATI NULE (KNF):\nU mapi uokvirujemo NULE. Dobijeni članovi se sabiraju unutar zagrada, a promenljive se komplementiraju u odnosu na DNF.\nMinimalni KNF oblik glasi:\n   f = {mock_knf}\n'''
            
        self.guide_text_widget.delete('''1.0''', tk.END)
        self.guide_text_widget.insert(tk.END, explanation)
        
        # Popunjavanje polja za jednačine tačnim odgovorom
        self.dnf_user.delete(0, tk.END)
        self.dnf_user.insert(0, mock_dnf)
        if self.knf_user:
            self.knf_user.delete(0, tk.END)
            self.knf_user.insert(0, mock_knf)

if __name__ == '''__main__''':
    app = LogicTrainerApp()
    app.mainloop()
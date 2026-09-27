import tkinter as tk
from tkinter import ttk
import random

class NumberSystemPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kviz i Vežba: Brojni Sistemi")
        
        # Pokretanje preko celog ekrana
        self.root.state('zoomed')
        self.root.configure(bg="#f4f6f9")
        
        # Definicija stilova
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_color = "#f4f6f9"
        self.card_color = "#ffffff"
        self.primary_color = "#2b5797"
        self.accent_color = "#00a300"
        self.danger_color = "#d9534f"
        self.text_color = "#333333"
        
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.primary_color, background=self.bg_color)
        
        self.style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background=self.primary_color)
        self.style.map("Action.TButton", background=[("active", "#1e3d6b")])
        
        self.style.configure("Check.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background=self.accent_color)
        self.style.map("Check.TButton", background=[("active", "#008a00")])

        # Varijable stanja
        self.current_type = tk.StringVar(value="DEC_TO_BIN")
        self.correct_ans = ""
        self.steps_data = {}
        
        self.setup_ui()
        self.generate_new_question()

    def setup_ui(self):
        # Gornji baner
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=70)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        lbl_title = tk.Label(header_frame, text="RADIX Brojni Sistemi - Edukativna Vežbaonica", 
                             fg="white", bg=self.primary_color, font=("Segoe UI", 18, "bold"))
        lbl_title.pack(pady=18, padx=20, anchor="w")

        # Glavni kontejner
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Leva strana: Biranje tipa zadatka
        sidebar = tk.LabelFrame(main_container, text=" Izaberite tip zadatka ", bg=self.bg_color, font=("Segoe UI", 11, "bold"), fg=self.primary_color)
        sidebar.pack(side="left", fill="y", padx=(0, 15), pady=5)
        
        types = [
            ("Dekadni u Binarni", "DEC_TO_BIN"),
            ("Binarni u Dekadni", "BIN_TO_DEC"),
            ("Binarni u Oktalni", "BIN_TO_OCT"),
            ("Binarni u Heksadekadni", "BIN_TO_HEX"),
            ("Pakovani BCD format", "PACKED_BCD"),
            ("Raspakovani BCD format", "UNPACKED_BCD"),
            ("Opšta RADIX konverzija", "GENERAL_RADIX")
        ]
        
        for text, mode in types:
            btn = tk.Radiobutton(sidebar, text=text, value=mode, variable=self.current_type,
                                 command=self.generate_new_question, bg=self.bg_color, activebackground=self.bg_color,
                                 font=("Segoe UI", 11), anchor="w", width=22, indicatoron=0, 
                                 selectcolor="#d1e1f7", bd=1, relief="groove", pady=8, padx=10)
            btn.pack(pady=5, padx=10, fill="x")

        # Desna strana: Radni prostor
        self.workspace = tk.Frame(main_container, bg=self.bg_color)
        self.workspace.pack(side="right", fill="both", expand=True, pady=5)
        
        # Kartica sa zadatkom
        self.card = tk.Frame(self.workspace, bg=self.card_color, bd=1, relief="solid")
        self.card.pack(fill="x", ipady=10, padx=5, pady=5)
        
        self.lbl_task_descr = tk.Label(self.card, text="ZADATAK:", bg=self.card_color, font=("Segoe UI", 11, "bold"), fg="#555555")
        self.lbl_task_descr.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.lbl_question = tk.Label(self.card, text="", bg=self.card_color, font=("Segoe UI", 14, "bold"), fg=self.primary_color)
        self.lbl_question.pack(anchor="w", padx=15, pady=(0, 5))

        # Radna tabela (Postupak)
        self.work_frame = tk.LabelFrame(self.workspace, text=" Postupak i radna tabela ", bg=self.bg_color, font=("Segoe UI", 11, "bold"), fg=self.primary_color)
        self.work_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        # Statusna traka
        self.status_frame = tk.Frame(self.workspace, bg=self.bg_color)
        self.status_frame.pack(fill="x", pady=5, padx=5)
        self.lbl_status = tk.Label(self.status_frame, text="", font=("Segoe UI", 12, "bold"), bg=self.bg_color, anchor="w")
        self.lbl_status.pack(fill="x", padx=5)
        
        # Donje kontrole i konačno rešenje
        self.ans_frame = tk.Frame(self.workspace, bg=self.bg_color)
        self.ans_frame.pack(fill="x", side="bottom", pady=5, padx=5)
        
        lbl_final_ans = tk.Label(self.ans_frame, text="Konačno rešenje:", font=("Segoe UI", 12, "bold"), bg=self.bg_color)
        lbl_final_ans.pack(side="left", padx=(0, 10))
        
        self.entry_final_ans = ttk.Entry(self.ans_frame, font=("Segoe UI", 13, "bold"), width=30)
        self.entry_final_ans.pack(side="left", padx=5, ipady=3)
        self.entry_final_ans.bind("<Return>", lambda event: self.check_answer())
        
        btn_check = ttk.Button(self.ans_frame, text="Proveri rešenje", style="Check.TButton", command=self.check_answer)
        btn_check.pack(side="left", padx=15)
        
        btn_next = ttk.Button(self.ans_frame, text="Sledeći zadatak", style="Action.TButton", command=self.generate_new_question)
        btn_next.pack(side="right", padx=5)

    def clear_work_frame(self):
        for widget in self.work_frame.winfo_children():
            widget.destroy()
        self.lbl_status.config(text="", bg=self.bg_color)

    def to_base(self, num, base):
        chars = "0123456789ABCDEF"
        if num == 0:
            return "0"
        res = []
        while num > 0:
            res.append(chars[num % base])
            num //= base
        return "".join(reversed(res))

    def generate_new_question(self):
        self.clear_work_frame()
        self.entry_final_ans.delete(0, tk.END)
        self.steps_data.clear()
        
        mode = self.current_type.get()
        
        if mode == "DEC_TO_BIN":
            num = random.randint(100, 1000)
            self.lbl_question.config(text=f"""Konvertovati dekadni broj ({num})10 u binarni broj.""")
            self.correct_ans = bin(num)[2:]
            
            lbl_info = tk.Label(self.work_frame, text="Delite broj sa 2, unosite količnik pa pritisnite ENTER za sledeći red:", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
            lbl_info.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)
            
            tk.Label(self.work_frame, text="Broj / Količnik", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=0, padx=10, pady=2)
            tk.Label(self.work_frame, text=": 2 =", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=1, padx=5, pady=2)
            tk.Label(self.work_frame, text="Novi Količnik", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=2, padx=10, pady=2)
            tk.Label(self.work_frame, text="Ostatak", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=3, padx=10, pady=2)
            
            self.steps_data["rows"] = []
            self.steps_data["current_active_row"] = 0
            
            temp = num
            all_steps = []
            while temp > 0:
                q_expected = temp // 2
                r_expected = temp % 2
                all_steps.append((temp, q_expected, r_expected))
                temp = q_expected
            
            self.steps_data["all_steps"] = all_steps
            self.show_next_division_row()
            
        elif mode == "BIN_TO_DEC":
            dec_num = random.randint(20, 255)
            bin_str = bin(dec_num)[2:]
            self.lbl_question.config(text=f"""Konvertovati binarni broj ({bin_str})2 u dekadni broj.""")
            self.correct_ans = str(dec_num)
            
            lbl_info = tk.Label(self.work_frame, text="Izračunajte vrednost svakog bita (zdesna nalevo od stepena 0). Pritisnite ENTER za sledeći bit:", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
            lbl_info.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=5)
            
            tk.Label(self.work_frame, text="Bit i njegova pozicija", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=0, padx=10, pady=2)
            tk.Label(self.work_frame, text="=", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=1, padx=5, pady=2)
            tk.Label(self.work_frame, text="Vrednost sabirka", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=2, padx=10, pady=2)
            
            all_steps = []
            for power, bit in enumerate(reversed(bin_str)):
                expected_val = int(bit) * (2 ** power)
                all_steps.append((bit, power, expected_val))
                
            self.steps_data["all_steps"] = all_steps
            self.steps_data["current_active_row"] = 0
            self.steps_data["rows"] = []
            self.show_next_binary_to_dec_row()

        elif mode in ["BIN_TO_OCT", "BIN_TO_HEX"]:
            dec_num = random.randint(200, 2000)
            bin_str = bin(dec_num)[2:]
            
            target_sys = "oktalni (baza 8)" if mode == "BIN_TO_OCT" else "heksadekadni (baza 16)"
            self.lbl_question.config(text=f"""Konvertovati binarni broj ({bin_str})2 u {target_sys} broj.""")
            self.correct_ans = oct(dec_num)[2:] if mode == "BIN_TO_OCT" else hex(dec_num)[2:].upper()
            
            group_size = 3 if mode == "BIN_TO_OCT" else 4
            lbl_info = tk.Label(self.work_frame, text=f"""Grupišite bitove po {group_size} cifre (zdesna nalevo) i prenesite vrednost:""", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
            lbl_info.pack(anchor="w", padx=15, pady=5)
            
            pad_len = (group_size - (len(bin_str) % group_size)) % group_size
            padded_bin = "0" * pad_len + bin_str
            groups = [padded_bin[i:i+group_size] for i in range(0, len(padded_bin), group_size)]
            
            tbl_frame = tk.Frame(self.work_frame, bg=self.bg_color)
            tbl_frame.pack(pady=15, padx=15, anchor="w")
            
            self.steps_data["entries"] = []
            self.steps_data["expected"] = []
            
            for col_idx, group in enumerate(groups):
                group_frame = tk.Frame(tbl_frame, bg="#eef2f7", bd=1, relief="solid", padx=15, pady=10)
                group_frame.pack(side="left", padx=8)
                
                tk.Label(group_frame, text=f"""Grupa {col_idx+1}""", font=("Segoe UI", 9, "bold"), fg="#666666", bg="#eef2f7").pack()
                tk.Label(group_frame, text=group, font=("Segoe UI", 13, "bold"), fg=self.primary_color, bg="#eef2f7").pack(pady=5)
                tk.Label(group_frame, text="Vrednost:", font=("Segoe UI", 9), bg="#eef2f7").pack()
                
                ent_val = tk.Entry(group_frame, width=6, font=("Segoe UI", 11, "bold"), justify="center", bd=1, relief="solid")
                ent_val.pack(pady=2)
                
                val_expected = str(int(group, 2)) if mode == "BIN_TO_OCT" else hex(int(group, 2))[2:].upper()
                self.steps_data["entries"].append(ent_val)
                self.steps_data["expected"].append(val_expected)
                
        elif mode in ["PACKED_BCD", "UNPACKED_BCD"]:
            num = random.randint(100, 9999)
            bcd_type = "pakovani (Packed - 4 bita)" if mode == "PACKED_BCD" else "raspakovani (Unpacked - 8 bita)"
            self.lbl_question.config(text=f"""Konvertovati dekadni broj {num} u {bcd_type} BCD format.""")
            
            digits = [int(d) for d in str(num)]
            bits_needed = 4 if mode == "PACKED_BCD" else 8
            self.correct_ans = " ".join([bin(d)[2:].zfill(bits_needed) for d in digits])
                
            lbl_info = tk.Label(self.work_frame, text="Zapišite binarni kod za svaku pojedinačnu cifru decimalnog broja:", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
            lbl_info.pack(anchor="w", padx=15, pady=5)
            
            tbl_frame = tk.Frame(self.work_frame, bg=self.bg_color)
            tbl_frame.pack(pady=15, padx=15, anchor="w")
            
            self.steps_data["entries"] = []
            self.steps_data["expected"] = []
            
            for digit in str(num):
                digit_frame = tk.Frame(tbl_frame, bg="#fcfcfc", bd=1, relief="solid", padx=15, pady=10)
                digit_frame.pack(side="left", padx=10)
                
                tk.Label(digit_frame, text="Cifra", font=("Segoe UI", 9), fg="#666666", bg="#fcfcfc").pack()
                tk.Label(digit_frame, text=str(digit), font=("Segoe UI", 18, "bold"), fg="#d00000", bg="#fcfcfc").pack(pady=2)
                tk.Label(digit_frame, text=f"""Binarno ({bits_needed}b):""", font=("Segoe UI", 9), bg="#fcfcfc").pack()
                
                ent_bcd = tk.Entry(digit_frame, width=12, font=("Segoe UI", 11, "bold"), justify="center", bd=1, relief="solid")
                ent_bcd.pack(pady=4)
                
                expected_bin = bin(int(digit))[2:].zfill(bits_needed)
                self.steps_data["entries"].append(ent_bcd)
                self.steps_data["expected"].append(expected_bin)

        elif mode == "GENERAL_RADIX":
            # Biramo nasumično smer: ili IZ baze 10 ili U bazu 10 (baze od 3 do 16, izuzev 10)
            available_bases = [3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16]
            chosen_base = random.choice(available_bases)
            direction = random.choice(["FROM_DEC", "TO_DEC"])
            
            dec_val = random.randint(30, 400)
            
            if direction == "FROM_DEC":
                # Zadatak: Iz baze 10 u izabranu bazu (Sukcesivno deljenje)
                self.lbl_question.config(text=f"""Konvertovati dekadni broj ({dec_val})10 u sistem sa bazom {chosen_base}.""")
                self.correct_ans = self.to_base(dec_val, chosen_base)
                self.steps_data["sub_mode"] = "DIVISION"
                
                lbl_info = tk.Label(self.work_frame, text=f"""Delite dekadni broj sa {chosen_base}, unosite količnik i ostatak pa pritisnite ENTER za sledeći red:""", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
                lbl_info.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)
                
                tk.Label(self.work_frame, text="Broj / Količnik", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=0, padx=10, pady=2)
                tk.Label(self.work_frame, text=f""": {chosen_base} =""", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=1, padx=5, pady=2)
                tk.Label(self.work_frame, text="Novi Količnik", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=2, padx=10, pady=2)
                tk.Label(self.work_frame, text="Ostatak", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=3, padx=10, pady=2)
                
                self.steps_data["rows"] = []
                self.steps_data["current_active_row"] = 0
                
                temp = dec_val
                all_steps = []
                while temp > 0:
                    q_expected = temp // chosen_base
                    r_raw = temp % chosen_base
                    r_expected = "0123456789ABCDEF"[r_raw] # podrška za slova A-F ako je baza > 10
                    all_steps.append((temp, q_expected, r_expected))
                    temp = q_expected
                
                self.steps_data["all_steps"] = all_steps
                self.show_next_general_div_row(chosen_base)
                
            else:
                # Zadatak: Iz izabrane baze u dekadnu bazu 10 (Suma sabiraka)
                base_str = self.to_base(dec_val, chosen_base)
                self.lbl_question.config(text=f"""Konvertovati broj ({base_str}){chosen_base} u dekadni broj.""")
                self.correct_ans = str(dec_val)
                self.steps_data["sub_mode"] = "SUM"
                
                lbl_info = tk.Label(self.work_frame, text=f"""Izračunajte vrednost svake cifre zdesna nalevo (cifra * {chosen_base}^stepen). Pritisnite ENTER za sledeći red:""", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
                lbl_info.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=5)
                
                tk.Label(self.work_frame, text="Cifra i njena pozicija", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=0, padx=10, pady=2)
                tk.Label(self.work_frame, text="=", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=1, padx=5, pady=2)
                tk.Label(self.work_frame, text="Vrednost sabirka (dekadno)", font=("Segoe UI", 10, "bold"), bg=self.bg_color).grid(row=1, column=2, padx=10, pady=2)
                
                all_steps = []
                chars = "0123456789ABCDEF"
                for power, char in enumerate(reversed(base_str)):
                    digit_val = chars.index(char)
                    expected_val = digit_val * (chosen_base ** power)
                    all_steps.append((char, power, expected_val, chosen_base))
                    
                self.steps_data["all_steps"] = all_steps
                self.steps_data["current_active_row"] = 0
                self.steps_data["rows"] = []
                self.show_next_general_sum_row()

    def show_next_division_row(self):
        active_idx = self.steps_data["current_active_row"]
        all_steps = self.steps_data["all_steps"]
        if active_idx >= len(all_steps): return
            
        temp, q_expected, r_expected = all_steps[active_idx]
        row_idx = active_idx + 2
        
        lbl_current = tk.Label(self.work_frame, text=str(temp), font=("Segoe UI", 11, "bold"), bg=self.bg_color)
        lbl_current.grid(row=row_idx, column=0, padx=10, pady=3)
        tk.Label(self.work_frame, text=": 2 =", bg=self.bg_color).grid(row=row_idx, column=1, padx=5, pady=3)
        
        ent_q = tk.Entry(self.work_frame, width=8, font=("Segoe UI", 10), bd=1, relief="solid")
        ent_q.grid(row=row_idx, column=2, padx=10, pady=3)
        ent_r = tk.Entry(self.work_frame, width=5, font=("Segoe UI", 10, "bold"), justify="center", bd=1, relief="solid")
        ent_r.grid(row=row_idx, column=3, padx=10, pady=3)
        
        ent_q.focus_set()
        ent_q.bind("<Return>", lambda e: self.validate_and_advance_row(ent_q, ent_r, q_expected, r_expected))
        ent_r.bind("<Return>", lambda e: self.validate_and_advance_row(ent_q, ent_r, q_expected, r_expected))
        self.steps_data["rows"].append((ent_q, ent_r, q_expected, r_expected))

    def validate_and_advance_row(self, ent_q, ent_r, q_exp, r_exp):
        u_q = ent_q.get().strip()
        u_r = ent_r.get().strip().upper()
        if u_q == str(q_exp) and u_r == str(r_exp):
            ent_q.config(bg="#d4edda", state="disabled")
            ent_r.config(bg="#d4edda", state="disabled")
            self.lbl_status.config(text="Tačan korak! Otvoren je sledeći red.", fg="#155724", bg="#d4edda")
            self.steps_data["current_active_row"] += 1
            if self.steps_data["current_active_row"] < len(self.steps_data["all_steps"]):
                self.show_next_division_row()
            else:
                self.lbl_status.config(text="Završeno deljenje! Upišite konačno rešenje odozdo nadole.", fg="#155724", bg="#d4edda")
                self.entry_final_ans.focus_set()
        else:
            ent_q.config(bg="#f8d7da" if u_q != str(q_exp) else "#d4edda")
            ent_r.config(bg="#f8d7da" if u_r != str(r_exp) else "#d4edda")
            self.lbl_status.config(text="Količnik ili ostatak nije tačan. Ispravite polje.", fg="#721c24", bg="#f8d7da")

    def show_next_binary_to_dec_row(self):
        active_idx = self.steps_data["current_active_row"]
        all_steps = self.steps_data["all_steps"]
        if active_idx >= len(all_steps): return
            
        bit, power, expected_val = all_steps[active_idx]
        row_idx = active_idx + 2
        
        lbl_current = tk.Label(self.work_frame, text=f"""{bit} * 2^{power}""", font=("Segoe UI", 11, "bold"), bg=self.bg_color)
        lbl_current.grid(row=row_idx, column=0, padx=10, pady=3, sticky="w")
        tk.Label(self.work_frame, text="=", bg=self.bg_color).grid(row=row_idx, column=1, padx=5, pady=3)
        
        ent_v = tk.Entry(self.work_frame, width=10, font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        ent_v.grid(row=row_idx, column=2, padx=10, pady=3)
        ent_v.focus_set()
        
        ent_v.bind("<Return>", lambda e: self.validate_and_advance_dec_row(ent_v, expected_val))
        self.steps_data["rows"].append((ent_v, expected_val))

    def validate_and_advance_dec_row(self, ent_v, expected_val):
        if ent_v.get().strip() == str(expected_val):
            ent_v.config(bg="#d4edda", state="disabled")
            self.lbl_status.config(text="Tačan sabirak! Idemo na sledeći stepen baze.", fg="#155724", bg="#d4edda")
            self.steps_data["current_active_row"] += 1
            if self.steps_data["current_active_row"] < len(self.steps_data["all_steps"]):
                self.show_next_binary_to_dec_row()
            else:
                self.lbl_status.config(text="Izračunali ste sve sabirke! Saberite ih za konačni dekadni rezultat.", fg="#155724", bg="#d4edda")
                self.entry_final_ans.focus_set()
        else:
            ent_v.config(bg="#f8d7da")
            self.lbl_status.config(text="Vrednost sabirka nije tačna.", fg="#721c24", bg="#f8d7da")

    def show_next_general_div_row(self, base_divisor):
        active_idx = self.steps_data["current_active_row"]
        all_steps = self.steps_data["all_steps"]
        if active_idx >= len(all_steps): return
        
        temp, q_expected, r_expected = all_steps[active_idx]
        row_idx = active_idx + 2
        
        lbl_current = tk.Label(self.work_frame, text=str(temp), font=("Segoe UI", 11, "bold"), bg=self.bg_color)
        lbl_current.grid(row=row_idx, column=0, padx=10, pady=3)
        tk.Label(self.work_frame, text=f""": {base_divisor} =""", bg=self.bg_color).grid(row=row_idx, column=1, padx=5, pady=3)
        
        ent_q = tk.Entry(self.work_frame, width=8, font=("Segoe UI", 10), bd=1, relief="solid")
        ent_q.grid(row=row_idx, column=2, padx=10, pady=3)
        ent_r = tk.Entry(self.work_frame, width=5, font=("Segoe UI", 10, "bold"), justify="center", bd=1, relief="solid")
        ent_r.grid(row=row_idx, column=3, padx=10, pady=3)
        
        ent_q.focus_set()
        ent_q.bind("<Return>", lambda e: self.validate_and_advance_gen_div(ent_q, ent_r, q_expected, r_expected, base_divisor))
        ent_r.bind("<Return>", lambda e: self.validate_and_advance_gen_div(ent_q, ent_r, q_expected, r_expected, base_divisor))
        self.steps_data["rows"].append((ent_q, ent_r, q_expected, r_expected))

    def validate_and_advance_gen_div(self, ent_q, ent_r, q_exp, r_exp, base_divisor):
        u_q = ent_q.get().strip()
        u_r = ent_r.get().strip().upper()
        if u_q == str(q_exp) and u_r == str(r_exp):
            ent_q.config(bg="#d4edda", state="disabled")
            ent_r.config(bg="#d4edda", state="disabled")
            self.lbl_status.config(text="Tačan korak deljenja! Otvoren je sledeći red.", fg="#155724", bg="#d4edda")
            self.steps_data["current_active_row"] += 1
            if self.steps_data["current_active_row"] < len(self.steps_data["all_steps"]):
                self.show_next_general_div_row(base_divisor)
            else:
                self.lbl_status.config(text="Završili ste deljenje! Unesite ostatke odozdo nadole u konačno rešenje.", fg="#155724", bg="#d4edda")
                self.entry_final_ans.focus_set()
        else:
            ent_q.config(bg="#f8d7da" if u_q != str(q_exp) else "#d4edda")
            ent_r.config(bg="#f8d7da" if u_r != str(r_exp) else "#d4edda")
            self.lbl_status.config(text="Količnik ili ostatak nije tačan.", fg="#721c24", bg="#f8d7da")

    def show_next_general_sum_row(self):
        active_idx = self.steps_data["current_active_row"]
        all_steps = self.steps_data["all_steps"]
        if active_idx >= len(all_steps): return
        
        char, power, expected_val, chosen_base = all_steps[active_idx]
        row_idx = active_idx + 2
        
        lbl_current = tk.Label(self.work_frame, text=f"""{char} * {chosen_base}^{power}""", font=("Segoe UI", 11, "bold"), bg=self.bg_color)
        lbl_current.grid(row=row_idx, column=0, padx=10, pady=3, sticky="w")
        tk.Label(self.work_frame, text="=", bg=self.bg_color).grid(row=row_idx, column=1, padx=5, pady=3)
        
        ent_v = tk.Entry(self.work_frame, width=10, font=("Segoe UI", 10, "bold"), bd=1, relief="solid")
        ent_v.grid(row=row_idx, column=2, padx=10, pady=3)
        ent_v.focus_set()
        
        ent_v.bind("<Return>", lambda e: self.validate_and_advance_gen_sum(ent_v, expected_val))
        self.steps_data["rows"].append((ent_v, expected_val))

    def validate_and_advance_gen_sum(self, ent_v, expected_val):
        if ent_v.get().strip() == str(expected_val):
            ent_v.config(bg="#d4edda", state="disabled")
            self.lbl_status.config(text="Tačan sabirak! Idemo na sledeću poziciju.", fg="#155724", bg="#d4edda")
            self.steps_data["current_active_row"] += 1
            if self.steps_data["current_active_row"] < len(self.steps_data["all_steps"]):
                self.show_next_general_sum_row()
            else:
                self.lbl_status.config(text="Svi sabirci su tačni! Saberite ih za konačni dekadni rezultat.", fg="#155724", bg="#d4edda")
                self.entry_final_ans.focus_set()
        else:
            ent_v.config(bg="#f8d7da")
            self.lbl_status.config(text="Vrednost sabirka u dekadnom sistemu nije tačna.", fg="#721c24", bg="#f8d7da")

    def check_answer(self):
        mode = self.current_type.get()
        steps_correct = True
        
        if mode in ["BIN_TO_OCT", "BIN_TO_HEX", "PACKED_BCD", "UNPACKED_BCD"]:
            for i, ent in enumerate(self.steps_data["entries"]):
                user_val = ent.get().strip().upper()
                exp_val = self.steps_data["expected"][i]
                if user_val == exp_val:
                    ent.config(bg="#d4edda")
                else:
                    ent.config(bg="#f8d7da")
                    steps_correct = False
        elif mode in ["DEC_TO_BIN", "BIN_TO_DEC", "GENERAL_RADIX"]:
            if self.steps_data["current_active_row"] < len(self.steps_data["all_steps"]):
                steps_correct = False

        final_user = self.entry_final_ans.get().strip().upper().replace(" ", "")
        final_correct_clean = self.correct_ans.upper().replace(" ", "")
        
        if final_user == final_correct_clean:
            if steps_correct:
                self.lbl_status.config(
                    text=f"""SVAKA ČAST! Sve je TAČNO! Kompletan postupak i konačni rezultat ({self.correct_ans}) su ispravni.""", 
                    fg="#155724", bg="#d4edda"
                )
            else:
                self.lbl_status.config(
                    text=f"""Konačan rezultat je TAČAN ({self.correct_ans}), ali niste završili sve korake u tabeli postupka!""", 
                    fg="#856404", bg="#fff3cd"
                )
        else:
            self.lbl_status.config(
                text=f"""NETAČNO! Vaš unos: {final_user if final_user else 'Prazno'}. Tačan odgovor: {self.correct_ans}. Proverite crvena polja.""", 
                fg="#721c24", bg="#f8d7da"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSystemPracticeApp(root)
    root.mainloop()
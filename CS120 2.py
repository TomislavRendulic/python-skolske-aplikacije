import tkinter as tk
from tkinter import ttk
import random

class CompleteAdvancedRepresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacija 2: Napredne Računarske Reprezentacije i IEEE 754")
        
        self.root.state('zoomed')
        self.root.configure(bg="#f4f6f9")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_color = "#f4f6f9"
        self.card_color = "#ffffff"
        self.primary_color = "#2b5797"
        self.accent_color = "#00a300"
        self.text_color = "#333333"
        
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.primary_color, background=self.bg_color)
        self.style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background=self.primary_color)
        self.style.map("Action.TButton", background=[("active", "#1e3d6b")])
        self.style.configure("Check.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background=self.accent_color)
        self.style.map("Check.TButton", background=[("active", "#008a00")])

        self.current_type = tk.StringVar(value="UNPACKED_SIGNED")
        self.correct_ans = ""
        self.steps_data = {}
        
        self.setup_ui()
        self.generate_new_question()

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=70)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        lbl_title = tk.Label(header_frame, text="Računarski Sistemi (Lekcija 2) - Interaktivno Učenje", 
                             fg="white", bg=self.primary_color, font=("Segoe UI", 18, "bold"))
        lbl_title.pack(pady=18, padx=20, anchor="w")

        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        sidebar = tk.LabelFrame(main_container, text=" Moduli Lekcije 2 ", bg=self.bg_color, font=("Segoe UI", 11, "bold"), fg=self.primary_color)
        sidebar.pack(side="left", fill="y", padx=(0, 15), pady=5)
        
        types = [
            ("Raspakovani BCD (Predznak)", "UNPACKED_SIGNED"),
            ("Prvi Komplement (1's)", "FIRST_COMPLEMENT"),
            ("Drugi Komplement (2's)", "SECOND_COMPLEMENT"),
            ("Predstavljanje sa Pomerajem", "OFFSET_BINARY"),
            ("IEEE 754 Standardni Format", "IEEE_754_STANDARD"),
            ("IEEE 754 Specijalne Vrednosti", "IEEE_754_SPECIAL")
        ]
        
        for text, mode in types:
            btn = tk.Radiobutton(sidebar, text=text, value=mode, variable=self.current_type,
                                 command=self.generate_new_question, bg=self.bg_color, activebackground=self.bg_color,
                                 font=("Segoe UI", 11), anchor="w", width=25, indicatoron=0, 
                                 selectcolor="#d1e1f7", bd=1, relief="groove", pady=8, padx=10)
            btn.pack(pady=5, padx=10, fill="x")

        self.workspace = tk.Frame(main_container, bg=self.bg_color)
        self.workspace.pack(side="right", fill="both", expand=True, pady=5)
        
        self.card = tk.Frame(self.workspace, bg=self.card_color, bd=1, relief="solid")
        self.card.pack(fill="x", ipady=10, padx=5, pady=5)
        
        self.lbl_task_descr = tk.Label(self.card, text="ZADATAK:", bg=self.card_color, font=("Segoe UI", 11, "bold"), fg="#555555")
        self.lbl_task_descr.pack(anchor="w", padx=15, pady=(5, 2))
        
        self.lbl_question = tk.Label(self.card, text="", bg=self.card_color, font=("Segoe UI", 14, "bold"), fg=self.primary_color)
        self.lbl_question.pack(anchor="w", padx=15, pady=(0, 5))

        self.canvas = tk.Canvas(self.workspace, bg=self.bg_color, bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.workspace, orient="vertical", command=self.canvas.yview)
        self.work_frame = tk.LabelFrame(self.canvas, text=" Interaktivni radni postupak (Validacija na ENTER / TAB) ", bg=self.bg_color, font=("Segoe UI", 11, "bold"), fg=self.primary_color)
        
        self.work_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.work_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=5, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)
        
        self.status_frame = tk.Frame(self.workspace, bg=self.bg_color)
        self.status_frame.pack(fill="x", side="bottom", pady=5, padx=5)
        self.lbl_status = tk.Label(self.status_frame, text="", font=("Segoe UI", 12, "bold"), bg=self.bg_color, anchor="w")
        self.lbl_status.pack(fill="x", padx=5)
        
        self.ans_frame = tk.Frame(self.workspace, bg=self.bg_color)
        self.ans_frame.pack(fill="x", side="bottom", pady=5, padx=5)
        
        lbl_final_ans = tk.Label(self.ans_frame, text="Konačni binarni zapis:", font=("Segoe UI", 12, "bold"), bg=self.bg_color)
        lbl_final_ans.pack(side="left", padx=(0, 10))
        
        self.entry_final_ans = ttk.Entry(self.ans_frame, font=("Segoe UI", 13, "bold"), width=35)
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

    def bind_validation(self, widget, callback):
        widget.bind("<Return>", lambda e: callback())
        widget.bind("<FocusOut>", lambda e: callback())

    def generate_new_question(self):
        self.clear_work_frame()
        self.entry_final_ans.delete(0, tk.END)
        self.steps_data.clear()
        
        mode = self.current_type.get()
        
        if mode == "UNPACKED_SIGNED":
            sign = random.choice(["+", "-"])
            num = random.randint(100, 999)
            self.lbl_question.config(text=f"Konvertovati broj {sign}{num} u raspakovani BCD format sa predznakom.")
            zone = "0000" if sign == "+" else "1000"
            self.correct_ans = " ".join([f"{zone}{bin(int(d))[2:].zfill(4)}" for d in str(num)])
            
            lbl_info = tk.Label(self.work_frame, text=f"Upišite punih 8 bita (zona + cifra) za svaku poziciju. Zona za {sign} je {zone}:", bg=self.bg_color, font=("Segoe UI", 10, "italic"))
            lbl_info.pack(anchor="w", padx=15, pady=5)
            
            tbl_frame = tk.Frame(self.work_frame, bg=self.bg_color)
            tbl_frame.pack(pady=15, padx=15, anchor="w")
            
            self.steps_data["entries"] = []
            self.steps_data["expected"] = []
            for d in str(num):
                d_frame = tk.Frame(tbl_frame, bg="#fcfcfc", bd=1, relief="solid", padx=15, pady=10)
                d_frame.pack(side="left", padx=10)
                tk.Label(d_frame, text=f"Cifra: {d}", font=("Segoe UI", 12, "bold"), bg="#fcfcfc").pack()
                ent = tk.Entry(d_frame, width=14, font=("Segoe UI", 11, "bold"), justify="center")
                ent.pack(pady=5)
                self.steps_data["entries"].append(ent)
                self.steps_data["expected"].append(f"{zone}{bin(int(d))[2:].zfill(4)}")
                
        elif mode == "FIRST_COMPLEMENT":
            length = random.choice([8, 12])
            bin_val = "".join(random.choice(["0", "1"]) for _ in range(length))
            self.lbl_question.config(text=f"Odrediti prvi komplement za binarni niz: ({bin_val})2")
            self.correct_ans = "".join("1" if b == "0" else "0" for b in bin_val)
            
            grid_frame = tk.Frame(self.work_frame, bg=self.bg_color)
            grid_frame.pack(pady=15, padx=15, anchor="w")
            
            self.steps_data["entries"] = []
            self.steps_data["expected"] = list(self.correct_ans)
            for idx, b in enumerate(bin_val):
                b_frame = tk.Frame(grid_frame, bg="#eef2f7", bd=1, relief="solid", width=45, height=60)
                b_frame.grid(row=0, column=idx, padx=2)
                b_frame.pack_propagate(False)
                tk.Label(b_frame, text=b, font=("Segoe UI", 11, "bold"), bg="#eef2f7").pack(pady=2)
                ent = tk.Entry(b_frame, width=3, font=("Segoe UI", 11, "bold"), justify="center")
                ent.pack(side="bottom", pady=4)
                self.steps_data["entries"].append(ent)

        elif mode == "SECOND_COMPLEMENT":
            bin_val = "".join(random.choice(["0", "1"]) for _ in range(8))
            self.lbl_question.config(text=f"Odrediti drugi komplement za 8-bitni binarni niz: ({bin_val})2")
            
            inverted = "".join("1" if b == "0" else "0" for b in bin_val)
            self.correct_ans = bin((int(inverted, 2) + 1) & 0xFF)[2:].zfill(8)
            
            carry = 1
            expected_carries = []
            expected_sums = []
            for i in range(7, -1, -1):
                inv_bit = int(inverted[i])
                s = inv_bit + carry
                expected_sums.append(str(s % 2))
                carry = s // 2
                expected_carries.append(str(carry))
                
            expected_sums.reverse()
            expected_carries.reverse()
            
            tbl = tk.Frame(self.work_frame, bg=self.bg_color)
            tbl.pack(padx=15, pady=15, anchor="w")
            
            tk.Label(tbl, text="Originalni binarni niz:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
            for i, b in enumerate(bin_val):
                tk.Label(tbl, text=b, font=("Segoe UI", 12, "bold"), fg="#555555").grid(row=0, column=2+i, padx=8)
                
            tk.Label(tbl, text="KORAK 1: Prvi komplement:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", pady=10)
            self.steps_data["inv_entries"] = []
            for i, b in enumerate(inverted):
                ent = tk.Entry(tbl, width=3, font=("Segoe UI", 11, "bold"), justify="center")
                ent.grid(row=1, column=2+i, pady=5)
                self.steps_data["inv_entries"].append((ent, b))
                
            # Pravilan redosled odozgo nadole: Prenos (Carry) je IZNAD rezultata sabiranja
            tk.Label(tbl, text="KORAK 2: Sabiranje sa +1 (Idite zdesna ulevo):", font=("Segoe UI", 10, "bold"), fg=self.primary_color).grid(row=2, column=0, columnspan=2, sticky="w", pady=10)
            
            tk.Label(tbl, text="Prenos (Carry):", font=("Segoe UI", 9, "italic"), fg="#b58100").grid(row=3, column=1, sticky="e")
            tk.Label(tbl, text="Rezultat (+1):", font=("Segoe UI", 11, "bold")).grid(row=4, column=1, sticky="e")
            
            self.steps_data["carry_entries"] = [None]*8
            self.steps_data["sum_entries"] = [None]*8
            self.steps_data["exp_sums"] = expected_sums
            self.steps_data["exp_carries"] = expected_carries
            
            for i in range(8):
                ent_c = tk.Entry(tbl, width=3, font=("Segoe UI", 9, "italic"), justify="center", bg="#fff3cd")
                ent_c.grid(row=3, column=2+i, pady=2)
                ent_s = tk.Entry(tbl, width=3, font=("Segoe UI", 11, "bold"), justify="center")
                ent_s.grid(row=4, column=2+i, pady=2)
                self.steps_data["carry_entries"][i] = ent_c
                self.steps_data["sum_entries"][i] = ent_s
                
            self.steps_data["current_add_pos"] = 7
            self.activate_next_addition_cell()

        elif mode == "OFFSET_BINARY":
            m = random.choice([5, 6, 7, 8])
            bias = 2 ** (m - 1)
            val = random.randint(-bias + 1, bias - 1)
            self.lbl_question.config(text=f"Napisati broj {val} u 'offset binary' reprezentaciji sa m = {m} bita.")
            
            shifted_val = val + bias
            self.correct_ans = bin(shifted_val)[2:].zfill(m)
            
            # Korak 1: Računanje samog pomeraja
            tk.Label(self.work_frame, text=f"1. Koliki je pomeraj (Bias) za m = {m} bita? (Formula: 2^(m-1)):", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=5)
            ent_bias = tk.Entry(self.work_frame, width=10, font=("Segoe UI", 11, "bold"))
            ent_bias.grid(row=0, column=1, sticky="w", pady=5)
            self.steps_data["ent_bias"] = ent_bias
            self.steps_data["exp_bias"] = str(bias)
            
            # Korak 2: Računanje pomerene dekadne vrednosti
            tk.Label(self.work_frame, text=f"2. Izračunajte pomerenu dekadnu vrednost ( {val} + Bias ):", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=15, pady=5)
            ent_shift = tk.Entry(self.work_frame, width=10, font=("Segoe UI", 11, "bold"), state="disabled")
            ent_shift.grid(row=1, column=1, sticky="w", pady=5)
            self.steps_data["ent_shift"] = ent_shift
            self.steps_data["exp_shift"] = str(shifted_val)
            
            # Korak 3: Tabela deljenja sa jasnim oznakama
            self.steps_data["div_frame"] = tk.Frame(self.work_frame, bg=self.bg_color)
            self.steps_data["div_frame"].grid(row=2, column=0, columnspan=3, padx=15, pady=10, sticky="w")
            
            self.steps_data["all_div_steps"] = []
            temp = shifted_val
            while temp > 0:
                self.steps_data["all_div_steps"].append((temp, temp // 2, temp % 2))
                temp //= 2
            if not self.steps_data["all_div_steps"]:
                self.steps_data["all_div_steps"].append((0, 0, 0))
                
            self.steps_data["current_div_row"] = 0
            self.bind_validation(ent_bias, self.validate_offset_bias)

        elif mode == "IEEE_754_STANDARD":
            sign_bit = random.choice(["0", "1"])
            sign_char = "-" if sign_bit == "1" else "+"
            whole = random.choice([4, 5, 8, 9, 12])
            frac_part = random.choice([0.25, 0.5, 0.75])
            real_val = whole + frac_part
            
            self.lbl_question.config(text=f"Predstaviti realni broj {sign_char}{real_val} u 32-bitnom formatu IEEE 754 standarda.")
            
            bin_w = bin(whole)[2:]
            bin_f = ""
            tf = frac_part
            while tf > 0 and len(bin_f) < 10:
                tf *= 2
                bin_f += str(int(tf))
                tf -= int(tf)
                
            exponent_raw = len(bin_w) - 1
            exponent_biased = exponent_raw + 127
            mantissa_raw = (bin_w + bin_f)[1:].ljust(23, "0")[:23]
            exp_bin = bin(exponent_biased)[2:].zfill(8)
            self.correct_ans = f"{sign_bit} {exp_bin} {mantissa_raw}"
            
            # 1. Znak
            tk.Label(self.work_frame, text="1. Odredite bit znaka broja (1 bit):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=2)
            ent_s = tk.Entry(self.work_frame, width=5, font=("Segoe UI", 11, "bold"))
            ent_s.pack(anchor="w", padx=30, pady=2)
            self.steps_data["ent_s"] = ent_s
            self.steps_data["exp_s"] = sign_bit
            
            # 2. Tabela za celi deo
            tk.Label(self.work_frame, text=f"2. Prevedite celi deo broja ({whole}) u binarni sistem sukcesivnim deljenjem sa 2:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=5)
            self.steps_data["whole_frame"] = tk.Frame(self.work_frame, bg=self.bg_color)
            self.steps_data["whole_frame"].pack(anchor="w", padx=30)
            
            self.steps_data["whole_steps"] = []
            tw = whole
            while tw > 0:
                self.steps_data["whole_steps"].append((tw, tw // 2, tw % 2))
                tw //= 2
            self.steps_data["curr_w_row"] = 0
            
            self.steps_data["frac_part_val"] = frac_part
            self.steps_data["exponent_raw_val"] = exponent_raw
            self.steps_data["exp_biased_val"] = exponent_biased
            self.steps_data["exp_bin_val"] = exp_bin
            self.steps_data["mantissa_val"] = mantissa_raw
            
            self.bind_validation(ent_s, self.validate_ieee_sign)

        elif mode == "IEEE_754_SPECIAL":
            spec_type = random.choice(["NULA", "POZITIVNA BESKONAČNOST", "NaN (Not a Number)"])
            self.lbl_question.config(text=f"Konstruisati specijalnu konfiguraciju za vrednost: '{spec_type}' prema IEEE 754 standardu.")
            
            f_spec = tk.Frame(self.work_frame, bg=self.bg_color)
            f_spec.pack(padx=15, pady=15, anchor="w")
            
            if spec_type == "NULA":
                self.correct_ans = "0 00000000 00000000000000000000000"
                v_exp = "00000000"
                v_frac = "sve nule"
                lbl_help = "Pravilo za NULU: Eksponent sadrži sve nule (00000000), a Frakcija takođe sadrži sve nule."
            elif spec_type == "POZITIVNA BESKONAČNOST":
                self.correct_ans = "0 11111111 00000000000000000000000"
                v_exp = "11111111"
                v_frac = "sve nule"
                lbl_help = "Pravilo za BESKONAČNOST: Eksponent sadrži sve jedinice (11111111), a Frakcija sadrži sve nule."
            else:
                self.correct_ans = "0 11111111 10000000000000000000000"
                v_exp = "11111111"
                v_frac = "različita od nule"
                lbl_help = "Pravilo za NaN: Eksponent sadrži sve jedinice (11111111), a Frakcija je različita od nule (bilo koji bit je 1)."
                
            tk.Label(f_spec, text=lbl_help, font=("Segoe UI", 11, "italic"), fg=self.primary_color).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0,15))
            
            tk.Label(f_spec, text="Znak bit (1b):", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=5, sticky="w")
            ent_s = tk.Entry(f_spec, width=4, font=("Segoe UI", 11, "bold"), justify="center")
            ent_s.grid(row=2, column=0, padx=5, pady=5)
            
            tk.Label(f_spec, text="Eksponent (8b):", font=("Segoe UI", 10, "bold")).grid(row=1, column=1, padx=5, sticky="w")
            ent_e = tk.Entry(f_spec, width=14, font=("Segoe UI", 11, "bold"), justify="center")
            ent_e.grid(row=2, column=1, padx=5, pady=5)
            
            tk.Label(f_spec, text="Frakcija opcija (Ukucaj tekst 'sve nule' ili 'razlicita od nule'):", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, padx=5, sticky="w")
            ent_f = tk.Entry(f_spec, width=22, font=("Segoe UI", 11, "bold"))
            ent_f.grid(row=2, column=2, padx=5, pady=5)
            
            self.steps_data["spec_fields"] = (ent_s, ent_e, ent_f, "0", v_exp, v_frac)
            self.bind_validation(ent_s, self.validate_spec_fields)
            self.bind_validation(ent_e, self.validate_spec_fields)
            self.bind_validation(ent_f, self.validate_spec_fields)

    # --- LOGIKA VODILJE I VALIDACIJE KORAKA ---
    def activate_next_addition_cell(self):
        pos = self.current_add_pos
        if pos < 0:
            self.lbl_status.config(text="Bravo! Završili ste sabiranje. Sastavite konačni ishod na dno.", fg="#155724", bg="#d4edda")
            self.entry_final_ans.focus_set()
            return
        self.steps_data["sum_entries"][pos].focus_set()
        self.steps_data["sum_entries"][pos].bind("<Return>", lambda e: self.validate_addition_step())
        self.steps_data["sum_entries"][pos].bind("<FocusOut>", lambda e: self.validate_addition_step())

    def validate_addition_step(self):
        pos = self.current_add_pos
        if pos < 0: return
        u_sum = self.steps_data["sum_entries"][pos].get().strip()
        u_carry = self.steps_data["carry_entries"][pos].get().strip()
        
        exp_s = self.steps_data["exp_sums"][pos]
        exp_c = self.steps_data["exp_carries"][pos]
        
        if u_sum == exp_s and (pos == 7 or u_carry == exp_c):
            self.steps_data["sum_entries"][pos].config(bg="#d4edda", state="disabled")
            self.steps_data["carry_entries"][pos].config(bg="#d4edda", state="disabled")
            self.current_add_pos -= 1
            self.activate_next_addition_cell()
        else:
            self.steps_data["sum_entries"][pos].config(bg="#f8d7da")
            self.steps_data["carry_entries"][pos].config(bg="#f8d7da")

    def validate_offset_bias(self):
        if self.steps_data["ent_bias"].get().strip() == self.steps_data["exp_bias"]:
            self.steps_data["ent_bias"].config(bg="#d4edda", state="disabled")
            self.steps_data["ent_shift"].config(state="normal")
            self.steps_data["ent_shift"].focus_set()
            self.bind_validation(self.steps_data["ent_shift"], self.validate_offset_shift)
        else:
            self.steps_data["ent_bias"].config(bg="#f8d7da")

    def validate_offset_shift(self):
        if self.steps_data["ent_shift"].get().strip() == self.steps_data["exp_shift"]:
            self.steps_data["ent_shift"].config(bg="#d4edda", state="disabled")
            f = self.steps_data["div_frame"]
            tk.Label(f, text="Trenutni broj", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5)
            tk.Label(f, text="Količnik (:2)", font=("Segoe UI", 9, "bold"), fg=self.primary_color).grid(row=0, column=1, padx=5)
            tk.Label(f, text="Ostatak", font=("Segoe UI", 9, "bold"), fg="#d00000").grid(row=0, column=2, padx=5)
            self.show_next_offset_div_row()
        else:
            self.steps_data["ent_shift"].config(bg="#f8d7da")

    def show_next_offset_div_row(self):
        idx = self.steps_data["current_div_row"]
        steps = self.steps_data["all_div_steps"]
        f = self.steps_data["div_frame"]
        if idx >= len(steps):
            self.lbl_status.config(text="Tabela završena! Upišite ostatke unazad (odozdo prema gore) na dno ekrana.", fg="#155724", bg="#d4edda")
            self.entry_final_ans.focus_set()
            return
        val, q, r = steps[idx]
        r_idx = idx + 1
        tk.Label(f, text=f"{val}", font=("Segoe UI", 10, "bold")).grid(row=r_idx, column=0, padx=5)
        eq = tk.Entry(f, width=8)
        eq.grid(row=r_idx, column=1, pady=2, padx=5)
        er = tk.Entry(f, width=5, font=("Segoe UI", 10, "bold"), justify="center")
        er.grid(row=r_idx, column=2, pady=2, padx=5)
        
        eq.focus_set()
        eq.bind("<Return>", lambda e: self.validate_offset_div(eq, er, q, r))
        eq.bind("<FocusOut>", lambda e: self.validate_offset_div(eq, er, q, r))
        er.bind("<Return>", lambda e: self.validate_offset_div(eq, er, q, r))
        er.bind("<FocusOut>", lambda e: self.validate_offset_div(eq, er, q, r))

    def validate_offset_div(self, eq, er, exp_q, exp_r):
        if eq.get().strip() == str(exp_q) and er.get().strip() == str(exp_r):
            eq.config(bg="#d4edda", state="disabled")
            er.config(bg="#d4edda", state="disabled")
            self.steps_data["current_div_row"] += 1
            self.show_next_offset_div_row()
        else:
            if eq.get().strip() != str(exp_q) and eq.get().strip() != "": eq.config(bg="#f8d7da")
            if er.get().strip() != str(exp_r) and er.get().strip() != "": er.config(bg="#f8d7da")

    # --- IEEE 754 KORAK PO KORAK VALIDACIJA ---
    def validate_ieee_sign(self):
        if self.steps_data["ent_s"].get().strip() == self.steps_data["exp_s"]:
            self.steps_data["ent_s"].config(bg="#d4edda", state="disabled")
            f = self.steps_data["whole_frame"]
            tk.Label(f, text="Broj", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5)
            tk.Label(f, text="Količnik", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5)
            tk.Label(f, text="Ostatak", font=("Segoe UI", 9, "bold"), fg="#d00000").grid(row=0, column=2, padx=5)
            self.show_next_ieee_whole_row()
        else:
            self.steps_data["ent_s"].config(bg="#f8d7da")

    def show_next_ieee_whole_row(self):
        idx = self.steps_data["curr_w_row"]
        steps = self.steps_data["whole_steps"]
        f = self.steps_data["whole_frame"]
        if idx >= len(steps):
            self.open_ieee_fraction_module()
            return
        val, q, r = steps[idx]
        r_idx = idx + 1
        tk.Label(f, text=f"{val}").grid(row=r_idx, column=0, padx=5)
        eq = tk.Entry(f, width=8)
        eq.grid(row=r_idx, column=1, pady=2, padx=5)
        er = tk.Entry(f, width=5, font=("Segoe UI", 10, "bold"), justify="center")
        er.grid(row=r_idx, column=2, pady=2, padx=5)
        
        eq.focus_set()
        eq.bind("<Return>", lambda e: self.validate_ieee_whole(eq, er, q, r))
        eq.bind("<FocusOut>", lambda e: self.validate_ieee_whole(eq, er, q, r))

    def validate_ieee_whole(self, eq, er, exp_q, exp_r):
        if eq.get().strip() == str(exp_q) and er.get().strip() == str(exp_r):
            eq.config(bg="#d4edda", state="disabled")
            er.config(bg="#d4edda", state="disabled")
            self.steps_data["curr_w_row"] += 1
            self.show_next_ieee_whole_row()
        else:
            eq.config(bg="#f8d7da")
            er.config(bg="#f8d7da")

    def open_ieee_fraction_module(self):
        tk.Label(self.work_frame, text="3. Pomnožite razlomljeni deo sa 2 da dobijete binarnu frakciju:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=5)
        self.steps_data["frac_frame"] = tk.Frame(self.work_frame, bg=self.bg_color)
        self.steps_data["frac_frame"].pack(anchor="w", padx=30)
        
        f = self.steps_data["frac_frame"]
        tk.Label(f, text="Vrednost", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(f, text="Proizvod (*2)", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5)
        tk.Label(f, text="Ceo deo (Bit)", font=("Segoe UI", 9, "bold"), fg=self.accent_color).grid(row=0, column=2, padx=5)
        
        self.steps_data["frac_steps"] = []
        tf = self.steps_data["frac_part_val"]
        while tf > 0 and len(self.steps_data["frac_steps"]) < 5:
            prod = tf * 2
            wb = int(prod)
            self.steps_data["frac_steps"].append((tf, prod, wb))
            tf = prod - wb
            
        self.steps_data["curr_f_row"] = 0
        self.show_next_ieee_frac_row()

    def show_next_ieee_frac_row(self):
        idx = self.steps_data["curr_f_row"]
        steps = self.steps_data["frac_steps"]
        f = self.steps_data["frac_frame"]
        if idx >= len(steps):
            self.open_ieee_exponent_calculation()
            return
        tf, prod, wb = steps[idx]
        r_idx = idx + 1
        tk.Label(f, text=f"{tf}").grid(row=r_idx, column=0, padx=5)
        ep = tk.Entry(f, width=10)
        ep.grid(row=r_idx, column=1, pady=2, padx=5)
        ew = tk.Entry(f, width=5, font=("Segoe UI", 10, "bold"), justify="center")
        ew.grid(row=r_idx, column=2, pady=2, padx=5)
        
        ep.focus_set()
        ep.bind("<Return>", lambda e: self.validate_ieee_frac(ep, ew, prod, wb))
        ep.bind("<FocusOut>", lambda e: self.validate_ieee_frac(ep, ew, prod, wb))

    def validate_ieee_frac(self, ep, ew, exp_p, exp_w):
        try: u_p = float(ep.get().strip())
        except: u_p = -1.0
        if abs(u_p - exp_p) < 0.001 and ew.get().strip() == str(exp_w):
            ep.config(bg="#d4edda", state="disabled")
            ew.config(bg="#d4edda", state="disabled")
            self.steps_data["curr_f_row"] += 1
            self.show_next_ieee_frac_row()
        else:
            ep.config(bg="#f8d7da")
            ew.config(bg="#f8d7da")

    def open_ieee_exponent_calculation(self):
        tk.Label(self.work_frame, text=f"4. Izračunajte pomereni Eksponent u dekadnoj bazi (Pomeraj sa slike je +127, formula: Sirovi_Exp {self.steps_data['exponent_raw_val']} + 127):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=5)
        ee10 = tk.Entry(self.work_frame, width=12, font=("Segoe UI", 11, "bold"))
        ee10.pack(anchor="w", padx=30, pady=2)
        self.steps_data["ee10"] = ee10
        ee10.focus_set()
        self.bind_validation(ee10, self.validate_ieee_exp10)

    def validate_ieee_exp10(self):
        if self.steps_data["ee10"].get().strip() == str(self.steps_data["exp_biased_val"]):
            self.steps_data["ee10"].config(bg="#d4edda", state="disabled")
            
            tk.Label(self.work_frame, text="5. Prevedite izračunatu vrednost eksponenta u 8-bitni binarni oblik sukcesivnim deljenjem sa 2:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=5)
            self.steps_data["exp_div_frame"] = tk.Frame(self.work_frame, bg=self.bg_color)
            self.steps_data["exp_div_frame"].pack(anchor="w", padx=30)
            
            f = self.steps_data["exp_div_frame"]
            tk.Label(f, text="Količnik", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5)
            tk.Label(f, text="Ostatak", font=("Segoe UI", 9, "bold"), fg="#d00000").grid(row=0, column=1, padx=5)
            
            self.steps_data["exp_div_steps"] = []
            te = self.steps_data["exp_biased_val"]
            while te > 0:
                self.steps_data["exp_div_steps"].append((te, te // 2, te % 2))
                te //= 2
            self.steps_data["curr_ed_row"] = 0
            self.show_next_ieee_exp_div_row()
        else:
            self.steps_data["ee10"].config(bg="#f8d7da")

    def show_next_ieee_exp_div_row(self):
        idx = self.steps_data["curr_ed_row"]
        steps = self.steps_data["exp_div_steps"]
        f = self.steps_data["exp_div_frame"]
        if idx >= len(steps):
            self.open_ieee_mantissa_field()
            return
        val, q, r = steps[idx]
        r_idx = idx + 1
        tk.Label(f, text=f"{val} : 2 = ").grid(row=r_idx, column=0, sticky="e")
        eq = tk.Entry(f, width=8)
        eq.grid(row=r_idx, column=1, pady=2, padx=5)
        er = tk.Entry(f, width=5, font=("Segoe UI", 10, "bold"), justify="center")
        er.grid(row=r_idx, column=2, pady=2, padx=5)
        
        eq.focus_set()
        eq.bind("<Return>", lambda e: self.validate_ieee_exp_div(eq, er, q, r))
        eq.bind("<FocusOut>", lambda e: self.validate_ieee_exp_div(eq, er, q, r))

    def validate_ieee_exp_div(self, eq, er, exp_q, exp_r):
        if eq.get().strip() == str(exp_q) and er.get().strip() == str(exp_r):
            eq.config(bg="#d4edda", state="disabled")
            er.config(bg="#d4edda", state="disabled")
            self.steps_data["curr_ed_row"] += 1
            self.show_next_ieee_exp_div_row()
        else:
            eq.config(bg="#f8d7da")

    def open_ieee_mantissa_field(self):
        tk.Label(self.work_frame, text="6. Iz dobijenih koraka (2 i 3) odbacite prvu vodeću jedinicu i upišite početak normalizovane Mantise (Prva 4 bita):", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=5)
        em = tk.Entry(self.work_frame, width=15, font=("Segoe UI", 11, "bold"))
        em.pack(anchor="w", padx=30, pady=2)
        self.steps_data["em_user"] = em
        em.focus_set()
        self.bind_validation(em, self.validate_ieee_mantissa_local)

    def validate_ieee_mantissa_local(self):
        u_m = self.steps_data["em_user"].get().strip()
        if self.steps_data["mantissa_val"].startswith(u_m) and len(u_m) >= 3:
            self.steps_data["em_user"].config(bg="#d4edda", state="disabled")
            self.lbl_status.config(text="Svi podkoraci su uspešni! Spojite komponente (Znak Eksponent Mantisa) u finalno polje ispod.", fg="#155724", bg="#d4edda")
            self.entry_final_ans.focus_set()
        else:
            self.steps_data["em_user"].config(bg="#f8d7da")

    def validate_spec_fields(self):
        e_s, e_e, e_f, s_exp, e_exp, f_exp = self.steps_data["spec_fields"]
        if e_s.get().strip() == s_exp: e_s.config(bg="#d4edda")
        else: e_s.config(bg="#f8d7da")
            
        if e_e.get().strip() == e_exp: e_e.config(bg="#d4edda")
        else: e_e.config(bg="#f8d7da")
            
        clean_f = e_f.get().strip().lower().replace("č", "c")
        exp_f_clean = f_exp.lower().replace("č", "c")
        if clean_f == exp_f_clean or (exp_f_clean == "sve nule" and clean_f == "0"):
            e_f.config(bg="#d4edda")
        else:
            e_f.config(bg="#f8d7da")

    # --- KONAČNA GLOBALNA PROVERA ---
    def check_answer(self):
        mode = self.current_type.get()
        steps_correct = True
        
        if mode == "UNPACKED_SIGNED":
            for i, ent in enumerate(self.steps_data["entries"]):
                if ent.get().strip().replace(" ", "") != self.steps_data["expected"][i]:
                    ent.config(bg="#f8d7da"); steps_correct = False
                else: ent.config(bg="#d4edda")
        elif mode == "FIRST_COMPLEMENT":
            for i, ent in enumerate(self.steps_data["entries"]):
                if ent.get().strip() != self.steps_data["expected"][i]:
                    ent.config(bg="#f8d7da"); steps_correct = False
                else: ent.config(bg="#d4edda")
        elif mode == "SECOND_COMPLEMENT":
            for ent, b in self.steps_data["inv_entries"]:
                if ent.get().strip() != b: ent.config(bg="#f8d7da"); steps_correct = False
            if self.current_add_pos >= 0: steps_correct = False
        elif mode == "OFFSET_BINARY":
            if "current_div_row" not in self.steps_data or self.steps_data["current_div_row"] < len(self.steps_data["all_div_steps"]):
                steps_correct = False
        elif mode == "IEEE_754_STANDARD":
            if "curr_ed_row" not in self.steps_data or self.steps_data["curr_ed_row"] < len(self.steps_data["exp_div_steps"]):
                steps_correct = False
        elif mode == "IEEE_754_SPECIAL":
            e_s, e_e, e_f, s_exp, e_exp, f_exp = self.steps_data["spec_fields"]
            clean_f = e_f.get().strip().lower().replace("č", "c")
            exp_f_clean = f_exp.lower().replace("č", "c")
            if e_s.get().strip() != s_exp or e_e.get().strip() != e_exp or (clean_f != exp_f_clean and not (exp_f_clean == "sve nule" and clean_f == "0")):
                steps_correct = False

        final_user = self.entry_final_ans.get().strip().upper().replace(" ", "")
        final_correct_clean = self.correct_ans.upper().replace(" ", "")
        
        if final_user == final_correct_clean or (mode == "IEEE_754_STANDARD" and final_user.startswith(final_correct_clean[:10])):
            if steps_correct:
                self.lbl_status.config(text=f"IZVRSNO! Sve je apsolutno tačno i postupak je ispravan. Rešenje: {self.correct_ans}", fg="#155724", bg="#d4edda")
            else:
                self.lbl_status.config(text="Konačan niz je tačan, ali popravite crvena/nedovršena polja u radnom postupku!", fg="#856404", bg="#fff3cd")
        else:
            self.lbl_status.config(text=f"NETAČNO! Proverite završni binarni niz. Očekivani rezultat: {self.correct_ans}", fg="#721c24", bg="#f8d7da")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompleteAdvancedRepresentationApp(root)
    root.mainloop()
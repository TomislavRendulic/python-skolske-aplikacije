import tkinter as tk
import sys
import random
import os
import json
from PIL import Image, ImageTk, ImageGrab

class Nastava:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#050505")
        
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.save_file = os.path.join(self.base_path, "study_os_data.json")
        self.podaci_lekcija_path = os.path.join(self.base_path, "lekcije.json")
        self.icon_path = os.path.join(self.base_path, "Nastava.ico")

        self.lesson_saves = self.load_saves()
        
        self.set_icons()

        self.predmeti = {
            "CS100": {"color": "#00FF7F", "img": "CS100.png", "title": "UVOD U PROGRAMIRANJE"},
            "MA120": {"color": "#00FFFF", "img": "MA120.png", "title": "LINEARNA ALGEBRA"},
            "NT110": {"color": "#FFFF00", "img": "NT110.png", "title": "POSLOVNA KOMUNIKACIJA"},
            "NT111": {"color": "#FF0000", "img": "NT111.png", "title": "ENGLESKI 1"},
            "SE101": {"color": "#FF4500", "img": "SE101.png", "title": "SOFTVERSKI INŽENJERING"}
        }

        self.penalty_text = "Velike su šanse da izlaskom iz ovog programa nastojim da gubim vreme na nešto drugo."
        self.in_penalty_mode = False
        self.escape_attempts = 0
        self.bar_images = []
        self.current_frame = None
        self.freeze_image = None

        self.exit_btn = tk.Button(self.root, text="izlaz...", fg="#111", bg="#050505", 
                                 font=("Arial", self.f_size(0.008)), relief="flat", command=self.show_penalty_screen)
        self.exit_btn.bind("<Enter>", self.handle_exit_hover)
        
        self.show_main_menu()
        self.force_focus()
        
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
        
    def set_icons(self):
        try:
            self.root.iconbitmap(self.icon_path)
            
            import ctypes
            myappid = 'mycompany.myproduct.subproduct.version' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Ikonica nije učitana: {e}")

    def f_size(self, ratio):
        return int(self.screen_h * ratio)

    def load_saves(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_progress(self, code, lesson, page):
        key = f"{code}_{lesson}"
        self.lesson_saves[key] = page
        with open(self.save_file, 'w') as f:
            json.dump(self.lesson_saves, f)

    def force_focus(self):
        if not self.in_penalty_mode and not getattr(self, 'typing_mode', False):
            self.root.focus_force()
        self.root.after(50, self.force_focus)

    def switch_frame(self):
        freeze_label = None
        if self.current_frame:
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            
            cap = ImageGrab.grab(bbox=(x, y, x+w, y+h))
            self.freeze_image = ImageTk.PhotoImage(cap)
            
            freeze_label = tk.Label(self.root, image=self.freeze_image, bg="#050505")
            freeze_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            freeze_label.lift()
            
            self.current_frame.destroy()

        new_frame = tk.Frame(self.root, bg="#050505")
        new_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.current_frame = new_frame
        
        if freeze_label:
            freeze_label.lift()
            self.root.after(50, freeze_label.destroy)
            
        self.exit_btn.lift()
        return new_frame

    def show_main_menu(self):
        container = self.switch_frame()
        self.in_penalty_mode = False
        self.escape_attempts = 0
        self.bar_images.clear()
        
        tk.Label(container, text="CHOOSE YOUR DESTINY", fg="#00FF7F", bg="#050505", 
                 font=("Courier New", self.f_size(0.04), "bold")).place(relx=0.5, rely=0.06, anchor="center")
        
        rel_w, gap = 0.17, 0.02
        start_x = (1 - (5 * rel_w + 4 * gap)) / 2
        bar_w_px = int(self.screen_w * rel_w)
        bar_h_px = int((bar_w_px * 7) / 4)
        
        for i, code in enumerate(self.predmeti.keys()):
            info = self.predmeti[code]
            current_x = start_x + (i * (rel_w + gap))
            img_path = self.resource_path(info["img"])
            
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((bar_w_px, bar_h_px), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.bar_images.append(photo)
                btn = tk.Button(container, image=photo, text=code, compound="center", fg="white", 
                                font=("Impact", self.f_size(0.035), "bold"), relief="flat", 
                                borderwidth=0, highlightthickness=0, bg="#050505", activebackground=info["color"],
                                command=lambda c=code: self.show_lessons_grid(c))
            else:
                btn = tk.Button(container, text=code, fg=info["color"], bg="#111", 
                                font=("Impact", self.f_size(0.035)), relief="flat", 
                                command=lambda c=code: self.show_lessons_grid(c))
            
            btn.place(relx=current_x, rely=0.12, relwidth=rel_w, relheight=bar_h_px/self.screen_h)
        self.spawn_exit()

    def show_lessons_grid(self, code):
        container = self.switch_frame()
        self.exit_btn.place_forget()
        info = self.predmeti[code]
        
        tk.Label(container, text=info["title"], fg=info["color"], bg="#050505", 
                 font=("Impact", self.f_size(0.06))).pack(pady=self.screen_h*0.04)
        
        grid_frame = tk.Frame(container, bg="#050505")
        grid_frame.pack(expand=True)
        
        for c in range(5): grid_frame.grid_columnconfigure(c, weight=1, uniform="lesson_btn")

        for i in range(1, 16):
            btn = tk.Button(grid_frame, text=f"LEKCIJA {i}", font=("Impact", self.f_size(0.025)), 
                            fg=info["color"], bg="#0a0a0a", relief="flat", activebackground=info["color"],
                            command=lambda c=code, l=i: self.open_lesson(c, l))
            btn.grid(row=(i-1)//5, column=(i-1)%5, padx=self.screen_w*0.025, pady=self.screen_h*0.025, sticky="nsew")

        tk.Button(container, text="POVRATAK", command=self.show_main_menu, 
                  fg="#444", bg="#050505", relief="flat", font=("Arial", self.f_size(0.015))).pack(pady=self.screen_h*0.02)

    def open_lesson(self, code, lesson_num):
            pages = []
            # Putanja do JSON-a
            if os.path.exists(self.podaci_lekcija_path):
                try:
                    with open(self.podaci_lekcija_path, 'r', encoding='utf-8') as f:
                        svi_podaci = json.load(f)
                        
                        # Prolazimo kroz sve ključeve u JSON-u (npr. "CS100_1_1", "CS100_1_2"...)
                        # i tražimo one koji pripadaju ovoj lekciji
                        prefix = f"{code}_{lesson_num}_"
                        relevantni_kljucevi = [k for k in svi_podaci.keys() if k.startswith(prefix)]
                        
                        # Sortiramo ključeve po broju na kraju (da idu 1, 2, 3...)
                        relevantni_kljucevi.sort(key=lambda x: int(x.split('_')[-1]))
                        
                        for k in relevantni_kljucevi:
                            podatak = svi_podaci[k]
                            pages.append({
                                "title": podatak.get("naslov", k), # Uzima naslov iz JSON-a
                                "type": podatak.get("tip", "GRADIVO")
                            })
                except Exception as e:
                    print(f"Greška pri čitanju podlekcija: {e}")

            # Ako je JSON prazan ili ne postoji, stavljamo placeholder da program ne pukne
            if not pages:
                pages = [{"title": "Nema podataka", "type": "GRADIVO"}]

            start_idx = self.lesson_saves.get(f"{code}_{lesson_num}", 0)
            # Osiguravamo da start_idx nije veći od broja pronađenih strana
            if start_idx >= len(pages): start_idx = 0
            
            self.render_page(code, pages, start_idx, lesson_num)

    def render_page(self, code, pages, idx, lesson_num):
        container = self.switch_frame()
        self.save_progress(code, lesson_num, idx)
        info = self.predmeti[code]
        
        data_key = f"{code}_{lesson_num}_{idx + 1}"
        lesson_data = {"tip": "GRADIVO", "naslov": pages[idx]["title"], "tekst": "Podaci nisu pronađeni."}
        
        if os.path.exists(self.podaci_lekcija_path):
            try:
                with open(self.podaci_lekcija_path, 'r', encoding='utf-8') as f:
                    svi_podaci = json.load(f)
                    lesson_data = svi_podaci.get(data_key, lesson_data)
            except Exception as e:
                lesson_data["tekst"] = f"Greška u JSON fajlu: {e}"

        self.typing_mode = True if "DOPUNJAVANJE" in lesson_data.get("tip", "") else False

        sidebar_w = self.screen_w * 0.25
        sidebar = tk.Frame(container, bg="#080808", width=sidebar_w)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="HIJERARHIJA", fg="#333", bg="#080808", font=("Impact", self.f_size(0.04))).pack(pady=self.f_size(0.02))
        
        for i, p in enumerate(pages):
            color = info["color"] if i == idx else "#444"
            tk.Button(sidebar, text=f"{'■' if p['type'] == 'GRADIVO' else '●'} {p['title']}", 
                      fg=color, bg="#080808", relief="flat", font=("Consolas", self.f_size(0.018)), anchor="w",
                      command=lambda x=i: self.render_page(code, pages, x, lesson_num)).pack(fill="x", padx=int(self.screen_w * 0.02), pady=self.f_size(0.005))

        canvas = tk.Canvas(container, bg="#050505", highlightthickness=0, borderwidth=0, highlightbackground="#050505")
        canvas.pack(side="left", expand=True, fill="both")
        scroll_frame = tk.Frame(canvas, bg="#050505")
        canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=self.screen_w * 0.6)

        def align_canvas(event):
            canvas.coords(canvas_window, (event.width - self.screen_w * 0.6) / 2, 0)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", align_canvas)

        def safe_scroll(event, c):
            if event.delta > 0 and c.yview()[0] <= 0: return
            c.yview_scroll(int(-1*(event.delta/120)), "units")

        tk.Label(scroll_frame, text=lesson_data.get("naslov", "BEZ NASLOVA").upper(), fg=info["color"], bg="#050505", 
                 font=("Impact", self.f_size(0.05)), wraplength=self.screen_w*0.55, justify="left").pack(anchor="w", pady=self.f_size(0.02))

        tip = lesson_data.get("tip", "GRADIVO")

        if tip == "GRADIVO":
            txt_area = tk.Text(scroll_frame, bg="#050505", fg="white", font=("Consolas", self.f_size(0.02)),
                               relief="flat", highlightthickness=0, wrap="word", cursor="arrow")
            txt_area.pack(fill="both", expand=True, padx=self.f_size(0.01))
            txt_area.tag_configure("bold", font=("Consolas", self.f_size(0.02), "bold"))
            txt_area.tag_configure("italic", font=("Consolas", self.f_size(0.02), "italic"))
            txt_area.tag_configure("under", underline=True)
            txt_area.tag_configure("napomena", font=("Consolas", self.f_size(0.016), "italic"), foreground="#888")
            txt_area.tag_configure("bullet", lmargin1=40, lmargin2=50)

            for el in lesson_data.get("elementi", []):
                stil = str(el.get("stil", "normal"))
                sadrzaj = str(el.get("sadrzaj", ""))
                podvuceno = str(el.get("podvuceno", ""))
                napomena = str(el.get("napomena", ""))
                novi_red = el.get("novi_red", True)
                

                if stil == "bold":
                    txt_area.insert("end", sadrzaj, "bold")
                    
                elif stil == "italic":
                    txt_area.insert("end", sadrzaj, "italic")
                    
                elif stil == "bullet":
                    if sadrzaj.strip():
                        txt_area.insert("end", f"  • {sadrzaj}", "bullet")
                    else:
                        txt_area.insert("end", "\n")
                    
                elif stil == "specijalno":
                    if napomena:
                        txt_area.insert("end", f" {napomena}", "napomena")
                        
                else:
                    txt_area.insert("end", sadrzaj)
                    
                if novi_red:
                    txt_area.insert("end", "\n")
            
            txt_area.update_idletasks()
            potrebna_visina = txt_area.count("1.0", "end", "displaylines")[0]
            txt_area.config(height=potrebna_visina)
            txt_area.config(state="disabled")

        elif tip == "TEST_ZAOKRUZIVANJE_MULTI":
            for q in lesson_data["pitanja"]:
                f = tk.Frame(scroll_frame, bg="#050505", pady=self.f_size(0.015)); f.pack(fill="x")
                tk.Label(f, text=q['tekst'], fg="white", bg="#050505", font=("Arial", self.f_size(0.022), "bold"), justify="left").pack(anchor="w")
                btns = []
                def proveri_z(oidx, tidx, blist):
                    if oidx == tidx:
                        for i, b in enumerate(blist): b.config(bg="#00FF7F" if i==tidx else "#FF4500", fg="black" if i==tidx else "white")
                    else:
                        blist[oidx].config(bg="#FF4500", fg="white")
                        sivi = [i for i, b in enumerate(blist) if b.cget("bg") == "#111"]
                        if len(sivi) == 1: blist[sivi[0]].config(bg="#00FF7F", fg="black")
                for i, opc in enumerate(q["opcije"]):
                    btn = tk.Button(f, text=opc, font=("Arial", self.f_size(0.018)), bg="#111", fg="white", relief="flat", anchor="w", padx=int(self.screen_w * 0.02), cursor="hand2")
                    btn.config(command=lambda idx=i, t=q['tacan'], bl=btns: proveri_z(idx, t, bl))
                    btn.pack(fill="x", pady=self.f_size(0.005)); btns.append(btn)

        elif tip == "TEST_TACNO_NETACNO_MULTI":
            for q in lesson_data["pitanja"]:
                f = tk.Frame(scroll_frame, bg="#050505", pady=self.f_size(0.01)); f.pack(fill="x")
                tk.Label(f, text=q['tekst'], fg="white", bg="#050505", font=("Arial", self.f_size(0.02)), wraplength=int(self.screen_w * 0.45), justify="left").pack(side="left")
                def p_tn(t, bt, bn):
                    bt.config(bg="#00FF7F" if t==0 else "#FF4500", fg="black" if t==0 else "white")
                    bn.config(bg="#00FF7F" if t==1 else "#FF4500", fg="black" if t==1 else "white")
                bt = tk.Button(f, text="TAČNO", bg="#111", fg="white", width=int(self.screen_w * 0.005), relief="flat", cursor="hand2")
                bn = tk.Button(f, text="NETAČNO", bg="#111", fg="white", width=int(self.screen_w * 0.005), relief="flat", cursor="hand2")
                bt.config(command=lambda t=q['tacan'], b1=bt, b2=bn: p_tn(t, b1, b2))
                bn.config(command=lambda t=q['tacan'], b1=bt, b2=bn: p_tn(t, b1, b2))
                bn.pack(side="right", padx=self.f_size(0.005)); bt.pack(side="right", padx=self.f_size(0.005))

        elif tip == "TEST_DOPUNJAVANJE_MULTI":
            for i, q in enumerate(lesson_data["pitanja"]):
                f = tk.Frame(scroll_frame, bg="#050505", pady=self.f_size(0.015)); f.pack(fill="x")
                tk.Label(f, text=q["prikaz"], fg="white", bg="#050505", font=("Arial", self.f_size(0.022))).pack(anchor="w")
                e = tk.Entry(f, font=("Consolas", self.f_size(0.022)), bg="#111", fg="white", insertbackground="white", relief="flat", highlightthickness=max(1, self.f_size(0.001)), cursor="xterm")
                e.pack(fill="x", pady=self.f_size(0.005)); 
                if i == 0: e.focus_set()
                e.bind("<Return>", lambda ev, ent=e, t=q['tacan']: ent.config(bg="#004400" if ent.get().strip().lower()==t.lower() else "#440000", fg="#00FF7F" if ent.get().strip().lower()==t.lower() else "#FF4500"))

        elif tip == "TEST_POVEZIVANJA":
            parovi = lesson_data.get("parovi", [])
            levi_delovi = [p["levo"] for p in parovi]
            desni_delovi = [p["desno"] for p in parovi]
            random.shuffle(desni_delovi)
            
            f_main = tk.Frame(scroll_frame, bg="#050505"); f_main.pack(fill="x", pady=self.f_size(0.02))
            self.matching_selected = None
            
            def match_logic(val, btn, side, correct_map):
                if not self.matching_selected:
                    self.matching_selected = {"val": val, "btn": btn, "side": side}
                    btn.config(bg="#333")
                else:
                    s = self.matching_selected
                    if s["side"] != side:
                        is_correct = False
                        if side == "R" and correct_map.get(s["val"]) == val: is_correct = True
                        if side == "L" and correct_map.get(val) == s["val"]: is_correct = True
                        
                        if is_correct:
                            btn.config(bg="#00FF7F", state="disabled")
                            s["btn"].config(bg="#00FF7F", state="disabled")
                        else:
                            btn.config(bg="#FF4500"); s["btn"].config(bg="#FF4500")
                            self.root.after(500, lambda b1=btn, b2=s["btn"]: (b1.config(bg="#111"), b2.config(bg="#111")))
                    else: s["btn"].config(bg="#111")
                    self.matching_selected = None

            c_map = {p["levo"]: p["desno"] for p in parovi}
            for i in range(len(parovi)):
                row = tk.Frame(f_main, bg="#050505", pady=self.f_size(0.005)); row.pack(fill="x")
                bl = tk.Button(row, text=levi_delovi[i], width=int(self.screen_w * 0.015), bg="#111", fg="white", 
                               relief="flat", font=("Arial", self.f_size(0.018)), pady=self.f_size(0.01))
                br = tk.Button(row, text=desni_delovi[i], width=int(self.screen_w * 0.02), bg="#111", fg="white", 
                               relief="flat", font=("Arial", self.f_size(0.018)), pady=self.f_size(0.01))
                
                bl.config(command=lambda v=levi_delovi[i], b=bl: match_logic(v, b, "L", c_map))
                br.config(command=lambda v=desni_delovi[i], b=br: match_logic(v, b, "R", c_map))
                bl.pack(side="left", padx=int(self.screen_w * 0.02)); br.pack(side="right", padx=int(self.screen_w * 0.02))

        elif tip == "TEST_KATEGORIZACIJE":
            kat = lesson_data["kategorije"]
            pitanja = lesson_data["pitanja"]
            curr_q = {"idx": 0}
            
            f_cat = tk.Frame(scroll_frame, bg="#050505", pady=self.f_size(0.02))
            f_cat.pack(fill="x")
            
            lbl_pojam = tk.Label(f_cat, text=pitanja[0]["pojam"], font=("Impact", self.f_size(0.04)), 
                                 fg="white", bg="#0a0a0a", pady=self.f_size(0.02), width=int(self.screen_w * 0.005))
            lbl_pojam.pack(pady=(0, self.f_size(0.1)))

            def sort_logic(c_idx, btn):
                tacan = pitanja[curr_q["idx"]]["tacan"]
                if c_idx == tacan:
                    original_bg = btn.cget("bg")
                    btn.config(bg="#00FF7F", fg="black")
                    
                    curr_q["idx"] += 1
                    if curr_q["idx"] < len(pitanja):
                        self.root.after(300, lambda: [
                            btn.config(bg=original_bg, fg="white"),
                            lbl_pojam.config(text=pitanja[curr_q["idx"]]["pojam"], fg="white")
                        ])
                    else:
                        lbl_pojam.config(text="ZAVRŠENO!", fg="#00FF7F")
                else:
                    original_bg = btn.cget("bg")
                    btn.config(bg="#FF4500")
                    lbl_pojam.config(fg="#FF4500")
                    self.root.after(300, lambda: [
                        btn.config(bg=original_bg),
                        lbl_pojam.config(fg="white")
                    ])

            btn_f = tk.Frame(f_cat, bg="#050505")
            btn_f.pack(pady=self.f_size(0.02))
            
            for i, k_ime in enumerate(kat):
                b = tk.Button(btn_f, text=k_ime.upper(), bg="#111", fg="white", 
                              font=("Arial", self.f_size(0.02), "bold"), 
                              padx=int(self.screen_w * 0.02), pady=self.f_size(0.02), relief="flat")
                b.config(command=lambda idx=i, btn=b: sort_logic(idx, btn))
                b.pack(side="left", padx=int(self.screen_w * 0.02))

        elif tip == "TEST_REDOSLED":
            ispravan = lesson_data["redosled"]
            pomesan = ispravan[:]
            random.shuffle(pomesan)
            f_red = tk.Frame(scroll_frame, bg="#050505", pady=self.f_size(0.02)); f_red.pack(fill="x")
            odabrani = []

            def red_logic(v, b):
                if v == ispravan[len(odabrani)]:
                    odabrani.append(v)
                    b.config(bg="#00FF7F", state="disabled", fg="black")
                else:
                    b.config(bg="#FF4500")
                    self.root.after(500, lambda btn=b: btn.config(bg="#111"))

            for korak in pomesan:
                btn = tk.Button(f_red, text=korak, bg="#111", fg="white", font=("Arial", self.f_size(0.018)), 
                                relief="flat", pady=self.f_size(0.01)); btn.pack(fill="x", pady=self.f_size(0.005))
                btn.config(command=lambda v=korak, b=btn: red_logic(v, b))

        scroll_frame.update_idletasks()
        container.bind_all("<MouseWheel>", lambda e: safe_scroll(e, canvas))
        footer = tk.Frame(container, bg="#0a0a0a", height=self.screen_h*0.06); footer.place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0)
        footer.grid_columnconfigure((0,1,2), weight=1, uniform="col")
        tk.Button(footer, text="PRETHODNA", bg="#111", fg="white" if idx > 0 else "#222", relief="flat", command=lambda: self.render_page(code, pages, idx-1, lesson_num) if idx > 0 else None).grid(row=0, column=0, sticky="nsew", padx=2, pady=self.f_size(0.005))
        tk.Button(footer, text="IZLAZ IZ LEKCIJE", bg=info["color"], fg="black", relief="flat", command=lambda: self.show_lessons_grid(code)).grid(row=0, column=1, sticky="nsew", padx=2, pady=self.f_size(0.005))
        tk.Button(footer, text="SLEDEĆA", bg="#111", fg="white" if idx < len(pages)-1 else "#222", relief="flat", command=lambda: self.render_page(code, pages, idx+1, lesson_num) if idx < len(pages)-1 else None).grid(row=0, column=2, sticky="nsew", padx=2, pady=self.f_size(0.005))
        
        scroll_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)
        
    def handle_exit_hover(self, e):
        if self.escape_attempts < 5:
            self.escape_attempts += 1
            self.spawn_exit()
        else: self.exit_btn.config(fg="#1a1a1a")

    def spawn_exit(self):
        self.exit_btn.place(relx=random.uniform(0.1, 0.9), rely=random.uniform(0.94, 0.97), anchor="center")

    def show_penalty_screen(self):
        container = self.switch_frame()
        self.exit_btn.place_forget()
        self.in_penalty_mode = True 
        
        hero_img_path = self.resource_path("Povratak u Bitku.png")
        
        if os.path.exists(hero_img_path):
            img = Image.open(hero_img_path).resize((int(self.screen_w*0.85), int(self.screen_h*0.5)), Image.Resampling.LANCZOS)
            self.hero_photo = ImageTk.PhotoImage(img)
            ret_btn = tk.Button(container, image=self.hero_photo, text="NAZAD NA UČENJE", compound="center", 
                               fg="white", font=("Impact", self.f_size(0.08), "bold"), command=self.show_main_menu, 
                               borderwidth=0, relief="flat", bg="black", activebackground="#111")
        else:
            ret_btn = tk.Button(container, text="NAZAD NA UČENJE", font=("Impact", self.f_size(0.06)), 
                                command=self.show_main_menu, bg="#111", fg="#00FF7F")
        ret_btn.place(relx=0.5, rely=0.38, anchor="center")

        p_frame = tk.Frame(container, bg="#000")
        p_frame.place(relx=0.5, rely=0.88, anchor="center", relwidth=0.9)
        tk.Label(p_frame, text=self.penalty_text, fg="#333", bg="#000", font=("Consolas", self.f_size(0.015))).pack()
        self.input_field = tk.Text(p_frame, font=("Consolas", self.f_size(0.02)), 
                                   bg="#0a0a0a", fg="#00FF7F", insertbackground="#00FF7F",
                                   height=int(self.screen_h * 0.002), wrap="word", relief="flat")
        self.input_field.pack(pady=self.f_size(0.01), fill="x", padx=self.screen_w*0.15)
        self.input_field.focus_set()
        tk.Button(p_frame, text="POTVRDI ODLAZAK", command=self.check_exit, fg="#1a1a1a", bg="#000", 
                  relief="flat", font=("Arial", self.f_size(0.012))).pack()

    def check_exit(self):
        uneti_tekst = self.input_field.get("1.0", "end-1c").strip()
        
        if uneti_tekst == self.penalty_text: 
            sys.exit()
        else:
            self.input_field.config(bg="red")
            self.root.after(200, lambda: self.input_field.config(bg="#0a0a0a"))
            self.input_field.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Nastava(root)
    root.mainloop()
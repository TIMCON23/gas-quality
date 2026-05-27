"""SCADA-like operator interface for Double Control monitoring."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .reconstruction import reconstruct_signal
from .anomalies.injection import inject_anomalies
from .double_control import double_control_full
from .config import DEFAULTS

TRANSLATIONS = {
    "en": {
        "title": "🔬 Double Control SCADA Operator Interface",
        "control_panel": "Control Panel",
        "load_raw": "Load Raw CSV",
        "reconstruct_signal": "Reconstruct Signal",
        "run_double_control": "Run Double Control",
        "export_report": "Export Report",
        "language": "Language",
        "signal_analysis": "Signal Analysis",
        "analysis_results": "Analysis Results",
        "status_idle": "Status: IDLE",
        "verdict": "Verdict: ---",
        "raw_reconstructed": "Raw: {raw}, Reconstructed: {recon}",
        "metric": "Metric",
        "value": "Value",
        "ready": "Ready",
        "loaded_raw_points": "Loaded {count} raw data points",
        "reconstruct_first": "Please reconstruct the signal first",
        "load_first": "Please load data first",
        "reconstruction_complete": "Reconstruction complete: {count} points",
        "analysis_complete": "Analysis complete. Raw points: {raw}, reconstructed points: {recon}, anomalies: {anoms}",
        "status_processing": "Status: PROCESSING...",
        "status_reconstructing": "Status: RECONSTRUCTING...",
        "status_complete": "Status: COMPLETE",
        "status_error": "Status: ERROR",
        "success": "Success",
        "warning": "Warning",
        "error": "Error",
        "loaded_raw_label": "Loaded {count} raw points",
        "reconstruction_complete": "Reconstruction complete: {count} points",
        "no_analysis_export": "No analysis to export",
        "report_exported": "Report exported to {file}",
        "reconstruct_button_hint": "Reconstruct the loaded signal",
        "raw_signal": "Raw Signal",
        "reconstructed_signal": "Reconstructed",
        "flow_m3h": "Flow (m³/h)",
        "signal_reconstruction": "Signal Reconstruction",
        "double_control_scores": "Double Control Scores",
        "sample_index": "Sample Index",
        "analysis_report_title": "DOUBLE CONTROL ANALYSIS REPORT",
        "total_points": "Total Points",
        "anomalies_found": "Anomalies Found",
        "anomaly_percent": "Anomaly Percentage",
        "l1_anomalies": "L1 Anomalies",
        "l2_anomalies": "L2 Anomalies",
        "l1_agreement": "L1-Agreement %",
        "control_mode": "Control Mode",
        "final_verdict": "Final Verdict",
        "normal": "✓ NORMAL",
        "l1_score": "L1 Statistical Score",
        "l2_score": "L2 Physical Score",
        "l1_threshold": "L1 Threshold",
        "l2_threshold": "L2 Threshold",
        "anomaly_score": "Anomaly Score",
        "anomaly_detected": "⚠️ ANOMALY DETECTED",
    },
    "de": {
        "title": "🔬 Double Control SCADA-Bedieneroberfläche",
        "control_panel": "Steuerungsfeld",
        "load_raw": "Roh-CSV laden",
        "reconstruct_signal": "Signal rekonstruieren",
        "run_double_control": "Double Control ausführen",
        "export_report": "Bericht exportieren",
        "language": "Sprache",
        "signal_analysis": "Signalanalyse",
        "analysis_results": "Analyseergebnisse",
        "status_idle": "Status: LEER",
        "verdict": "Urteil: ---",
        "raw_reconstructed": "Roh: {raw}, Rekonstruiert: {recon}",
        "metric": "Metrik",
        "value": "Wert",
        "ready": "Bereit",
        "loaded_raw_points": "Geladene Rohdaten: {count}",
        "reconstruct_first": "Bitte zuerst das Signal rekonstruieren",
        "load_first": "Bitte zuerst Daten laden",
        "reconstruction_complete": "Rekonstruktion abgeschlossen: {count} Punkte",
        "analysis_complete": "Analyse abgeschlossen. Rohpunkte: {raw}, rekonstruierte Punkte: {recon}, Anomalien: {anoms}",
        "status_processing": "Status: VERARBEITUNG...",
        "status_reconstructing": "Status: REKONSTRUIERUNG...",
        "status_complete": "Status: ABGESCHLOSSEN",
        "status_error": "Status: FEHLER",
        "success": "Erfolg",
        "warning": "Warnung",
        "error": "Fehler",
        "loaded_raw_label": "Geladene Rohdaten: {count}",
        "reconstruction_complete": "Rekonstruktion abgeschlossen: {count} Punkte",
        "no_analysis_export": "Keine Analyse zum Exportieren",
        "report_exported": "Bericht exportiert nach {file}",
        "reconstruct_button_hint": "Rekonstruiere das geladene Signal",
        "raw_signal": "Rohsignal",
        "reconstructed_signal": "Rekonstruiert",
        "flow_m3h": "Volumenstrom (m³/h)",
        "signal_reconstruction": "Signalrekonstruktion",
        "double_control_scores": "Double Control Wertungen",
        "sample_index": "Probenindex",
        "analysis_report_title": "DOUBLE CONTROL ANALYSEBERICHT",
        "total_points": "Gesamtpunkte",
        "anomalies_found": "Gefundene Anomalien",
        "anomaly_percent": "Anomalie %",
        "l1_anomalies": "L1 Anomalien",
        "l2_anomalies": "L2 Anomalien",
        "l1_agreement": "L1-Übereinstimmung %",
        "control_mode": "Steuermodus",
        "final_verdict": "Endgültiges Urteil",
        "normal": "✓ NORMAL",
        "l1_score": "L1 Statistische Bewertung",
        "l2_score": "L2 Physikalische Bewertung",
        "l1_threshold": "L1 Schwellenwert",
        "l2_threshold": "L2 Schwellenwert",
        "anomaly_score": "Anomalienbewertung",
        "anomaly_detected": "⚠️ ANOMALIE ERKANNT",
    },
    "es": {
        "title": "🔬 Interfaz SCADA Double Control",
        "control_panel": "Panel de Control",
        "load_raw": "Cargar CSV sin procesar",
        "reconstruct_signal": "Reconstruir Señal",
        "run_double_control": "Ejecutar Double Control",
        "export_report": "Exportar Informe",
        "language": "Idioma",
        "signal_analysis": "Análisis de Señal",
        "analysis_results": "Resultados del Análisis",
        "status_idle": "Estado: INACTIVO",
        "verdict": "Veredicto: ---",
        "raw_reconstructed": "Bruto: {raw}, Reconstruido: {recon}",
        "metric": "Métrica",
        "value": "Valor",
        "ready": "Listo",
        "loaded_raw_points": "Cargados {count} puntos en bruto",
        "reconstruct_first": "Por favor reconstruya la señal primero",
        "load_first": "Por favor cargue los datos primero",
        "reconstruction_complete": "Reconstrucción completa: {count} puntos",
        "analysis_complete": "Análisis completo. Puntos brutos: {raw}, puntos reconstruidos: {recon}, anomalías: {anoms}",
        "status_processing": "Estado: PROCESANDO...",
        "status_reconstructing": "Estado: RECONSTRUYENDO...",
        "status_complete": "Estado: COMPLETO",
        "status_error": "Estado: ERROR",
        "success": "Éxito",
        "warning": "Advertencia",
        "error": "Error",
        "loaded_raw_label": "Cargados {count} puntos en bruto",
        "reconstruction_complete": "Reconstrucción completa: {count} puntos",
        "no_analysis_export": "No hay análisis para exportar",
        "report_exported": "Informe exportado a {file}",
        "reconstruct_button_hint": "Reconstruye la señal cargada",
        "raw_signal": "Señal cruda",
        "reconstructed_signal": "Reconstruido",
        "flow_m3h": "Flujo (m³/h)",
        "signal_reconstruction": "Reconstrucción de señal",
        "double_control_scores": "Puntuaciones Double Control",
        "sample_index": "Índice de muestra",
        "analysis_report_title": "INFORME DE ANÁLISIS DOUBLE CONTROL",
        "total_points": "Puntos Totales",
        "anomalies_found": "Anomalías Encontradas",
        "anomaly_percent": "Porcentaje Anomalía",
        "l1_anomalies": "Anomalías L1",
        "l2_anomalies": "Anomalías L2",
        "l1_agreement": "Acuerdo L1 %",
        "control_mode": "Modo de Control",
        "final_verdict": "Veredicto Final",
        "normal": "✓ NORMAL",
        "l1_score": "Puntuación Estadística L1",
        "l2_score": "Puntuación Física L2",
        "l1_threshold": "Umbral L1",
        "l2_threshold": "Umbral L2",
        "anomaly_score": "Puntuación de Anomalía",
        "anomaly_detected": "⚠️ ANOMALÍA DETECTADA",
    },
    "pl": {
        "title": "🔬 Interfejs operatora SCADA Double Control",
        "control_panel": "Panel sterowania",
        "load_raw": "Załaduj surowe CSV",
        "reconstruct_signal": "Odtwórz sygnał",
        "run_double_control": "Uruchom Double Control",
        "export_report": "Eksportuj raport",
        "language": "Język",
        "signal_analysis": "Analiza sygnału",
        "analysis_results": "Wyniki analizy",
        "status_idle": "Stan: IDLE",
        "verdict": "Werdykt: ---",
        "raw_reconstructed": "Surowe: {raw}, Odtworzone: {recon}",
        "metric": "Metryka",
        "value": "Wartość",
        "ready": "Gotowy",
        "loaded_raw_points": "Wczytano {count} surowych punktów",
        "reconstruct_first": "Najpierw proszę odtworzyć sygnał",
        "load_first": "Najpierw proszę załadować dane",
        "reconstruction_complete": "Rekonstrukcja zakończona: {count} punktów",
        "analysis_complete": "Analiza zakończona. Surowe punkty: {raw}, odtworzone punkty: {recon}, anomalie: {anoms}",
        "status_processing": "Stan: PRZETWARZANIE...",
        "status_reconstructing": "Stan: ODTWARZANIE...",
        "status_complete": "Stan: ZAKOŃCZONO",
        "status_error": "Stan: BŁĄD",
        "success": "Sukces",
        "warning": "Ostrzeżenie",
        "error": "Błąd",
        "loaded_raw_label": "Wczytano {count} surowych punktów",
        "reconstruction_complete": "Rekonstrukcja zakończona: {count} punktów",
        "no_analysis_export": "Brak analizy do wyeksportowania",
        "report_exported": "Raport wyeksportowano do {file}",
        "reconstruct_button_hint": "Odtwórz załadowany sygnał",
        "raw_signal": "Sygnał surowy",
        "reconstructed_signal": "Odtworzony",
        "flow_m3h": "Przepływ (m³/h)",
        "signal_reconstruction": "Rekonstrukcja sygnału",
        "double_control_scores": "Wyniki Double Control",
        "sample_index": "Indeks próbki",
        "analysis_report_title": "RAPORT ANALIZY DOUBLE CONTROL",
        "total_points": "Punkty całkowite",
        "anomalies_found": "Wykryte anomalie",
        "anomaly_percent": "Procent anomalii",
        "l1_anomalies": "Anomalie L1",
        "l2_anomalies": "Anomalie L2",
        "l1_agreement": "Zgodność L1 %",
        "control_mode": "Tryb kontroli",
        "final_verdict": "Ostateczny werdykt",
        "normal": "✓ NORMALNE",
        "l1_score": "Wynik statystyczny L1",
        "l2_score": "Wynik fizyczny L2",
        "l1_threshold": "Próg L1",
        "l2_threshold": "Próg L2",
        "anomaly_score": "Wynik anomalii",
        "anomaly_detected": "⚠️ WYKRYTO ANOMALIĘ",
    },
    "uk": {
        "title": "🔬 SCADA-інтерфейс Double Control",
        "control_panel": "Панель управління",
        "load_raw": "Завантажити вхідний CSV",
        "reconstruct_signal": "Реконструювати сигнал",
        "run_double_control": "Запустити Double Control",
        "export_report": "Експортувати звіт",
        "language": "Мова",
        "signal_analysis": "Аналіз сигналу",
        "analysis_results": "Результати аналізу",
        "status_idle": "Статус: ГОТОВО",
        "verdict": "Вердикт: ---",
        "raw_reconstructed": "Сирі: {raw}, Реконструйовані: {recon}",
        "metric": "Метрика",
        "value": "Значення",
        "ready": "Готово",
        "loaded_raw_points": "Завантажено {count} вхідних точок",
        "reconstruct_first": "Будь ласка, спочатку реконструюйте сигнал",
        "load_first": "Будь ласка, спочатку завантажте дані",
        "reconstruction_complete": "Реконструкція завершена: {count} точок",
        "analysis_complete": "Аналіз завершено. Сирі точки: {raw}, реконструйовані точки: {recon}, аномалії: {anoms}",
        "status_processing": "Статус: ОБРОБКА...",
        "status_reconstructing": "Статус: РЕКОНСТРУКЦІЯ...",
        "status_complete": "Статус: ЗАВЕРШЕНО",
        "status_error": "Статус: ПОМИЛКА",
        "success": "Успіх",
        "warning": "Увага",
        "error": "Помилка",
        "loaded_raw_label": "Завантажено {count} вхідних точок",
        "reconstruction_complete": "Реконструкція завершена: {count} точок",
        "no_analysis_export": "Немає аналізу для експорту",
        "report_exported": "Звіт експортовано до {file}",
        "reconstruct_button_hint": "Реконструюйте завантажений сигнал",
        "raw_signal": "Сирий сигнал",
        "reconstructed_signal": "Реконструйований",
        "flow_m3h": "Потік (м³/год)",
        "signal_reconstruction": "Реконструкція сигналу",
        "double_control_scores": "Оцінки Double Control",
        "sample_index": "Індекс зразка",
        "analysis_report_title": "ЗВІТ АНАЛІЗУ DOUBLE CONTROL",
        "total_points": "Загальна кількість точок",
        "anomalies_found": "Виявлено аномалій",
        "anomaly_percent": "Відсоток аномалій",
        "l1_anomalies": "Аномалії L1",
        "l2_anomalies": "Аномалії L2",
        "l1_agreement": "Узгодженість L1 %",
        "control_mode": "Режим контролю",
        "final_verdict": "Кінцевий вердикт",
        "normal": "✓ НОРМАЛЬНО",
        "l1_score": "Статистична оцінка L1",
        "l2_score": "Фізична оцінка L2",
        "l1_threshold": "Поріг L1",
        "l2_threshold": "Поріг L2",
        "anomaly_score": "Оцінка аномалії",
        "anomaly_detected": "⚠️ ВИЯВЛЕНО АНОМАЛІЮ",
    }
}


def _translate(key, lang="en", **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs)


class DoubleControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 Double Control SCADA Operator Interface")
        self.root.geometry("1400x900")
        
        self.signal_raw = None
        self.signal_reconstructed = None
        self.time_raw = None
        self.df_metrics = None
        self.report = None
        self.lang = "en"
        
        self._build_ui()
    
    def _build_ui(self):
        # Top control panel
        control_frame = ttk.LabelFrame(self.root, text=self._t("control_panel"), padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.control_frame = control_frame
        self.load_button = ttk.Button(control_frame, text=self._t("load_raw"), command=self._load_data)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.reconstruct_button = ttk.Button(control_frame, text=self._t("reconstruct_signal"), command=self._reconstruct_signal)
        self.reconstruct_button.pack(side=tk.LEFT, padx=5)
        
        self.run_button = ttk.Button(control_frame, text=self._t("run_double_control"), command=self._run_analysis)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(control_frame, text=self._t("export_report"), command=self._export_report)
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        self.lang_label = ttk.Label(control_frame, text=self._t("language") + ":")
        self.lang_label.pack(side=tk.LEFT, padx=(20, 5))
        self.lang_var = tk.StringVar(value=self.lang)
        self.lang_combo = ttk.Combobox(control_frame, textvariable=self.lang_var, state="readonly", width=10)
        self.lang_combo["values"] = ["English", "Deutsch", "Español", "Polski", "Українська"]
        self.lang_combo.current(0)
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_change)
        
        # Main content: left (graph) + right (table)
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left: graph canvas
        self.left_frame = ttk.LabelFrame(content_frame, text=self._t("signal_analysis"), padding=5)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas_frame = ttk.Frame(self.left_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Right: status + table
        self.right_frame = ttk.LabelFrame(content_frame, text=self._t("analysis_results"), padding=5)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        
        # Status indicators
        self.status_label = ttk.Label(self.right_frame, text=self._t("status_idle"), foreground="gray")
        self.status_label.pack(pady=5)

        self.verdict_label = ttk.Label(self.right_frame, text=self._t("verdict"), font=("Arial", 12, "bold"))
        self.verdict_label.pack(pady=5)

        self.point_count_label = ttk.Label(self.right_frame, text=self._t("raw_reconstructed", raw=0, recon=0))
        self.point_count_label.pack(pady=5)

        # Metrics table
        self.tree = ttk.Treeview(self.right_frame, height=15, columns=("Metric", "Value"), show="headings")
        self.tree.column("Metric", width=120)
        self.tree.column("Value", width=100)
        self.tree.heading("Metric", text=self._t("metric"))
        self.tree.heading("Value", text=self._t("value"))
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text=self._t("ready"), relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _t(self, key, **kwargs):
        return _translate(key, self.lang, **kwargs)
    
    def _on_language_change(self, event=None):
        selection = self.lang_combo.get()
        lang_map = {
            "English": "en",
            "Deutsch": "de",
            "Español": "es",
            "Polski": "pl",
            "Українська": "uk",
        }
        self.lang = lang_map.get(selection, "en")
        self._apply_language()
    
    def _apply_language(self):
        self.root.title(self._t("title"))
        self.control_frame.config(text=self._t("control_panel"))
        self.left_frame.config(text=self._t("signal_analysis"))
        self.right_frame.config(text=self._t("analysis_results"))
        self.load_button.config(text=self._t("load_raw"))
        self.reconstruct_button.config(text=self._t("reconstruct_signal"))
        self.run_button.config(text=self._t("run_double_control"))
        self.export_button.config(text=self._t("export_report"))
        self.lang_label.config(text=self._t("language") + ":")
        self.status_label.config(text=self._t("status_idle"), foreground="gray")
        self.verdict_label.config(text=self._t("verdict"))
        self.point_count_label.config(text=self._t("raw_reconstructed", raw=(len(self.signal_raw) if self.signal_raw is not None else 0), recon=(len(self.signal_reconstructed) if self.signal_reconstructed is not None else 0)))
        self.status_bar.config(text=self._t("ready"))
        self.tree.heading("Metric", text=self._t("metric"))
        self.tree.heading("Value", text=self._t("value"))
        self.lang_combo.set({"en": "English", "de": "Deutsch", "es": "Español", "pl": "Polski", "uk": "Українська"}[self.lang])
        self.root.update_idletasks()
    
    def _load_data(self):
        try:
            file = filedialog.askopenfilename(initialdir=DEFAULTS["rec_file"].parent,
                                              filetypes=[("CSV files", "*.csv")])
            if file:
                df = pd.read_csv(file)
                self.time_raw = df["time"].values.astype(float) if "time" in df.columns else np.arange(len(df))
                self.signal_raw = df["black"].values.astype(float)
                self.signal_reconstructed = None
                self.point_count_label.config(text=self._t("raw_reconstructed", raw=len(self.signal_raw), recon=0))
                self.status_bar.config(text=self._t("loaded_raw_label", count=len(self.signal_raw)))
                messagebox.showinfo(self._t("success"), self._t("loaded_raw_points", count=len(self.signal_raw)))
        except Exception as e:
            messagebox.showerror(self._t("error"), str(e))
    
    def _run_analysis(self):
        if self.signal_raw is None:
            messagebox.showwarning(self._t("warning"), self._t("load_first"))
            return
        if self.signal_reconstructed is None:
            messagebox.showwarning(self._t("warning"), self._t("reconstruct_first"))
            return
        
        try:
            self.status_label.config(text=self._t("status_processing"), foreground="orange")
            self.root.update()
            
            # Create dummy metrics (or load from file)
            n = len(self.signal_reconstructed)
            self.df_metrics = pd.DataFrame({
                "flow_m3h": self.signal_reconstructed,
                "pressure_kpa": 410 + 5*np.random.randn(n),
                "temp_c": 15 + 2*np.sin(np.arange(n)*2*np.pi/n),
                "Qin": 250 + 10*np.random.randn(n),
                "Qout": 100 + 5*np.random.randn(n),
                "Qcons": 100 + 5*np.random.randn(n),
                "Qacc": 50 + 2*np.random.randn(n),
            })
            
            # Run Double Control
            self.report = double_control_full(
                self.signal_raw,
                self.signal_reconstructed,
                self.df_metrics,
                stat_threshold=0.6,
                phys_threshold=0.7,
                final_mode="weighted"
            )
            
            # Update UI
            self._update_results()
            self._plot_signals()
            
            self.status_label.config(text=self._t("status_complete"), foreground="green")
            self.status_bar.config(text=self._t("analysis_complete", raw=len(self.signal_raw), recon=len(self.signal_reconstructed), anoms=self.report['Final_Decision']['anomaly_count']))
            
        except Exception as e:
            messagebox.showerror(self._t("error"), str(e))
            self.status_label.config(text=self._t("status_error"), foreground="red")

    def _reconstruct_signal(self):
        if self.signal_raw is None:
            messagebox.showwarning(self._t("warning"), self._t("load_first"))
            return
        
        try:
            self.status_label.config(text=self._t("status_reconstructing"), foreground="orange")
            self.root.update()
            
            if hasattr(self, "time_raw") and self.time_raw is not None:
                _, self.signal_reconstructed = reconstruct_signal(self.time_raw, self.signal_raw)
            else:
                _, self.signal_reconstructed = reconstruct_signal(np.arange(len(self.signal_raw)), self.signal_raw)
            
            self.point_count_label.config(text=self._t("raw_reconstructed", raw=len(self.signal_raw), recon=len(self.signal_reconstructed)))
            self.status_bar.config(text=self._t("reconstruction_complete", count=len(self.signal_reconstructed)))
            self.status_label.config(text=self._t("status_complete"), foreground="green")
            self._plot_signals()
        except Exception as e:
            messagebox.showerror(self._t("error"), str(e))
            self.status_label.config(text=self._t("status_error"), foreground="red")
    
    def _update_results(self):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Populate with metrics
        if self.report:
            summary = self.report["Summary"]
            final = self.report["Final_Decision"]
            l1 = self.report["L1_Statistical"]
            l2 = self.report["L2_Physical"]
            
            metrics = [
                (self._t("total_points"), f"{summary['total_points']}"),
                (self._t("anomalies_found"), f"{final['anomaly_count']}"),
                (self._t("anomaly_percent"), f"{summary['anomaly_percentage']:.1f}%"),
                (self._t("l1_anomalies"), f"{l1['anomaly_count']}"),
                (self._t("l2_anomalies"), f"{l2['anomaly_count']}"),
                (self._t("l1_agreement"), f"{summary['l1_agreement']:.1f}%"),
                (self._t("control_mode"), final['mode']),
                (self._t("final_verdict"), final['verdict']),
            ]
            
            for metric, value in metrics:
                self.tree.insert("", "end", values=(metric, value))
            
            # Update verdict label
            if final['verdict'] == "ANOMALY DETECTED":
                self.verdict_label.config(text=self._t("anomaly_detected"), foreground="red")
            else:
                self.verdict_label.config(text=self._t("normal"), foreground="green")
    
    def _plot_signals(self):
        if self.signal_reconstructed is None:
            return
        
        # Clear previous plot
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Create figure with subplots
        fig = Figure(figsize=(8, 5), dpi=100)
        
        # Plot 1: Signals
        ax1 = fig.add_subplot(211)
        ax1.plot(self.signal_raw, label=self._t("raw_signal"), alpha=0.7)
        ax1.plot(self.signal_reconstructed, label=self._t("reconstructed_signal"), linewidth=2)
        ax1.set_ylabel(self._t("flow_m3h"))
        ax1.set_title(self._t("signal_reconstruction"))
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Anomaly score
        if self.report:
            ax2 = fig.add_subplot(212)
            l1_scores = self.report["L1_Statistical"]["scores"]
            l2_scores = self.report["L2_Physical"]["scores"]
            ax2.plot(l1_scores, label=self._t("l1_score"), alpha=0.7)
            ax2.plot(l2_scores, label=self._t("l2_score"), alpha=0.7)
            ax2.axhline(0.6, linestyle='--', color='r', label=self._t("l1_threshold"))
            ax2.axhline(0.7, linestyle='--', color='orange', label=self._t("l2_threshold"))
            ax2.set_ylabel(self._t("anomaly_score"))
            ax2.set_xlabel(self._t("sample_index"))
            ax2.set_title(self._t("double_control_scores"))
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim([0, 1])
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _export_report(self):
        if self.report is None:
            messagebox.showwarning(self._t("warning"), self._t("no_analysis_export"))
            return
        
        try:
            file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write("=" * 60 + "\n")
                    f.write(self._t("analysis_report_title") + "\n")
                    f.write("=" * 60 + "\n\n")
                    
                    summary = self.report["Summary"]
                    final = self.report["Final_Decision"]
                    l1 = self.report["L1_Statistical"]
                    l2 = self.report["L2_Physical"]
                    
                    f.write(f"{self._t('total_points')}: {summary['total_points']}\n")
                    f.write(f"{self._t('anomalies_found')}: {final['anomaly_count']}\n")
                    f.write(f"{self._t('anomaly_percent')}: {summary['anomaly_percentage']:.2f}%\n\n")
                    
                    f.write(self._t('analysis_report_title') + "\n")
                    f.write(f"{self._t('l1_anomalies')}: {l1['anomaly_count']}\n")
                    f.write(f"  {self._t('value')}: {l1['details']}\n\n")
                    
                    f.write(self._t('analysis_report_title') + "\n")
                    f.write(f"{self._t('l2_anomalies')}: {l2['anomaly_count']}\n")
                    f.write(f"  {self._t('value')}: {l2['details']}\n\n")
                    
                    f.write(f"{self._t('final_verdict')}: {final['verdict']}\n")
                
                messagebox.showinfo(self._t("success"), self._t("report_exported", file=file))
        except Exception as e:
            messagebox.showerror(self._t("error"), str(e))


def launch_gui():
    """Entry point for SCADA GUI."""
    root = tk.Tk()
    app = DoubleControlGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()


import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# قاموس اللغات (العربية، الإنجليزية، الفرنسية، الإسبانية)
LANGUAGES = {
    'العربية': {
        'title': 'جامع الملفات FileGatherer',
        'ext_label': 'اختر صيغة الملفات المطلوب جمعها:',
        'custom_ext_hint': 'أو اكتب امتداداً مخصصاً (مثال: .mp4):',
        'src_label': 'حدد مجلد البحث (المصدر):',
        'dst_label': 'حدد مجلد الحفظ (الوجهة):',
        'btn_browse': 'استعراض',
        'btn_run': 'بدء الجمع والنسخ',
        'lang_label': 'اللغة / Language:',
        'success': 'تم بنجاح! تم العثور على ونسخ {} ملف.',
        'err_fill': 'الرجاء تحديد مجلد البحث ومجلد الحفظ!',
        'err_path': 'المجلد المحدد غير موجود!',
        'err_unknown': 'حدث خطأ أثناء البحث:',
        'all_files': 'جميع الملفات (*.*)',
        'videos': 'مقاطع فيديو (.mp4, .mkv, .avi, .mov)',
        'images': 'صور (.jpg, .jpeg, .png, .gif, .svg)',
        'texts': 'ملفات نصية (.txt, .docx, .doc, .rtf)',
        'pdf': 'مستندات PDF (.pdf)',
        'audio': 'ملفات صوتية (.mp3, .wav, .flac, .aac)',
        'archives': 'ملفات مضغوطة (.zip, .rar, .7z, .tar)',
        'custom': 'صيغة مخصصة (أدخلها أدناه)',
    },
    'English': {
        'title': 'FileGatherer - جامع الملفات',
        'ext_label': 'Select File Format to Gather:',
        'custom_ext_hint': 'Or enter a custom extension (e.g. .mp4):',
        'src_label': 'Select Search Directory (Source):',
        'dst_label': 'Select Save Directory (Destination):',
        'btn_browse': 'Browse',
        'btn_run': 'Start Gathering',
        'lang_label': 'Language / اللغة:',
        'success': 'Success! Found and copied {} files.',
        'err_fill': 'Please select both source and destination folders!',
        'err_path': 'Selected folder does not exist!',
        'err_unknown': 'An error occurred during search:',
        'all_files': 'All Files (*.*)',
        'videos': 'Video Files (.mp4, .mkv, .avi, .mov)',
        'images': 'Image Files (.jpg, .jpeg, .png, .gif, .svg)',
        'texts': 'Text Files (.txt, .docx, .doc, .rtf)',
        'pdf': 'PDF Documents (.pdf)',
        'audio': 'Audio Files (.mp3, .wav, .flac, .aac)',
        'archives': 'Archive Files (.zip, .rar, .7z, .tar)',
        'custom': 'Custom Extension (Enter below)',
    },
    'Français': {
        'title': 'FileGatherer - Collecteur de Fichiers',
        'ext_label': 'Sélect. le format de fichier à rassembler:',
        'custom_ext_hint': 'Ou entrez une extension personnalisée (ex: .mp4):',
        'src_label': 'Dossier de recherche (Source):',
        'dst_label': 'Dossier de destination (Cible):',
        'btn_browse': 'Parcourir',
        'btn_run': 'Démarrer la collecte',
        'lang_label': 'Langue / Language:',
        'success': 'Succès! {} fichiers trouvés et copiés.',
        'err_fill': 'Veuillez sélectionner les dossiers source et cible!',
        'err_path': 'Le dossier sélectionné n\'existe pas!',
        'err_unknown': 'Une erreur est survenue:',
        'all_files': 'Tous les fichiers (*.*)',
        'videos': 'Fichiers Vidéo (.mp4, .mkv, .avi)',
        'images': 'Images (.jpg, .png, .gif)',
        'texts': 'Documents texte (.txt, .docx)',
        'pdf': 'Documents PDF (.pdf)',
        'audio': 'Fichiers Audio (.mp3, .wav)',
        'archives': 'Archives (.zip, .rar, .7z)',
        'custom': 'Extension personnalisée',
    },
    'Español': {
        'title': 'FileGatherer - Recopilador de Archivos',
        'ext_label': 'Seleccione el formato de archivo:',
        'custom_ext_hint': 'O ingrese una extensión personalizada (ej: .mp4):',
        'src_label': 'Carpeta de búsqueda (Origen):',
        'dst_label': 'Carpeta de destino (Guardar):',
        'btn_browse': 'Examinar',
        'btn_run': 'Iniciar Recopilación',
        'lang_label': 'Idioma / Language:',
        'success': '¡Éxito! Se encontraron y copiaron {} archivos.',
        'err_fill': (
            '¡Por favor seleccione las carpetas de origen y destino!'
        ),
        'err_path': '¡La carpeta seleccionada no existe!',
        'err_unknown': 'Ocurrió un error:',
        'all_files': 'Todos los archivos (*.*)',
        'videos': 'Archivos de Video (.mp4, .mkv, .avi)',
        'images': 'Imágenes (.jpg, .png, .gif)',
        'texts': 'Archivos de Texto (.txt, .docx)',
        'pdf': 'Documentos PDF (.pdf)',
        'audio': 'Archivos de Audio (.mp3, .wav)',
        'archives': 'Archivos Comprimidos (.zip, .rar)',
        'custom': 'Extensión personalizada',
    },
}

# خريطة الامتدادات البرمجية
EXT_MAP = {
    'all_files': [],  # كل الملفات
    'videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'texts': ['.txt', '.docx', '.doc', '.pdf', '.rtf', '.csv'],
    'pdf': ['.pdf'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
}


class FileGathererApp:

  def __init__(self, root):
    self.root = root
    self.current_lang = 'العربية'

    # إعداد الألوان (Black & White Theme)
    self.bg_color = '#000000'  # خلفية سوداء
    self.fg_color = '#FFFFFF'  # نص أبيض
    self.entry_bg = '#1A1A1A'  # رمادي داكن للحقول
    self.btn_bg = '#FFFFFF'  # أزرار بيضاء
    self.btn_fg = '#000000'  # نص زر أسود

    self.root.title('جامع الملفات FileGatherer')
    self.root.geometry('580x580')
    self.root.configure(bg=self.bg_color)
    self.root.resizable(False, False)

    self.setup_ui()
    self.update_language()

  def setup_ui(self):
    # شريط اختيار اللغة في الأعلى
    top_frame = tk.Frame(self.root, bg=self.bg_color)
    top_frame.pack(fill=tk.X, padx=20, pady=10)

    self.lbl_lang = tk.Label(
        top_frame, bg=self.bg_color, fg='#888888', font=('Arial', 9)
    )
    self.lbl_lang.pack(side=tk.LEFT)

    self.lang_combo = ttk.Combobox(
        top_frame,
        values=list(LANGUAGES.keys()),
        state='readonly',
        width=12,
    )
    self.lang_combo.set('العربية')
    self.lang_combo.pack(side=tk.LEFT, padx=5)
    self.lang_combo.bind('<<ComboboxSelected>>', self.on_lang_change)

    # العنوان الرئيسي للتطبيق (أبيض وأسود)
    self.title_label = tk.Label(
        self.root,
        text='جامع الملفات FileGatherer',
        bg=self.bg_color,
        fg=self.fg_color,
        font=('Arial', 16, 'bold'),
    )
    self.title_label.pack(pady=10)

    # فاصل خط أبيض
    separator = tk.Frame(self.root, bg='#333333', height=2)
    separator.pack(fill=tk.X, padx=20, pady=5)

    # --- صيغ الملفات ---
    self.lbl_ext = tk.Label(
        self.root,
        bg=self.bg_color,
        fg=self.fg_color,
        font=('Arial', 10, 'bold'),
    )
    self.lbl_ext.pack(anchor='w', padx=25, pady=(10, 2))

    self.ext_combo = ttk.Combobox(self.root, state='readonly', width=58)
    self.ext_combo.pack(padx=25, pady=2)
    self.ext_combo.bind('<<ComboboxSelected>>', self.on_ext_change)

    self.lbl_custom_ext = tk.Label(
        self.root, bg=self.bg_color, fg='#AAAAAA', font=('Arial', 8)
    )
    self.lbl_custom_ext.pack(anchor='w', padx=25, pady=(5, 2))

    self.custom_ext_entry = tk.Entry(
        self.root,
        bg=self.entry_bg,
        fg=self.fg_color,
        insertbackground='white',
        width=61,
        font=('Arial', 10),
    )
    self.custom_ext_entry.pack(padx=25, pady=2)

    # --- مجلد البحث ---
    self.lbl_src = tk.Label(
        self.root,
        bg=self.bg_color,
        fg=self.fg_color,
        font=('Arial', 10, 'bold'),
    )
    self.lbl_src.pack(anchor='w', padx=25, pady=(15, 2))

    src_frame = tk.Frame(self.root, bg=self.bg_color)
    src_frame.pack(fill=tk.X, padx=25, pady=2)

    self.src_entry = tk.Entry(
        src_frame,
        bg=self.entry_bg,
        fg=self.fg_color,
        insertbackground='white',
        width=48,
        font=('Arial', 10),
    )
    self.src_entry.pack(side=tk.LEFT, padx=(0, 5))

    self.btn_src = tk.Button(
        src_frame,
        bg=self.btn_bg,
        fg=self.btn_fg,
        activebackground='#CCCCCC',
        font=('Arial', 9, 'bold'),
        command=self.select_source,
    )
    self.btn_src.pack(side=tk.LEFT)

    # --- مجلد الحفظ ---
    self.lbl_dst = tk.Label(
        self.root,
        bg=self.bg_color,
        fg=self.fg_color,
        font=('Arial', 10, 'bold'),
    )
    self.lbl_dst.pack(anchor='w', padx=25, pady=(15, 2))

    dst_frame = tk.Frame(self.root, bg=self.bg_color)
    dst_frame.pack(fill=tk.X, padx=25, pady=2)

    self.dst_entry = tk.Entry(
        dst_frame,
        bg=self.entry_bg,
        fg=self.fg_color,
        insertbackground='white',
        width=48,
        font=('Arial', 10),
    )
    self.dst_entry.pack(side=tk.LEFT, padx=(0, 5))

    self.btn_dst = tk.Button(
        dst_frame,
        bg=self.btn_bg,
        fg=self.btn_fg,
        activebackground='#CCCCCC',
        font=('Arial', 9, 'bold'),
        command=self.select_destination,
    )
    self.btn_dst.pack(side=tk.LEFT)

    # --- زر التشغيل الرئيسي ---
    self.btn_run = tk.Button(
        self.root,
        bg='#FFFFFF',
        fg='#000000',
        activebackground='#DDDDDD',
        font=('Arial', 12, 'bold'),
        height=2,
        command=self.run_search,
    )
    self.btn_run.pack(fill=tk.X, padx=25, pady=25)

  def on_lang_change(self, event):
    self.current_lang = self.lang_combo.get()
    self.update_language()

  def update_language(self):
    lang_data = LANGUAGES[self.current_lang]

    self.title_label.config(text=lang_data['title'])
    self.lbl_lang.config(text=lang_data['lang_label'])
    self.lbl_ext.config(text=lang_data['ext_label'])
    self.lbl_custom_ext.config(text=lang_data['custom_ext_hint'])
    self.lbl_src.config(text=lang_data['src_label'])
    self.lbl_dst.config(text=lang_data['dst_label'])
    self.btn_src.config(text=lang_data['btn_browse'])
    self.btn_dst.config(text=lang_data['btn_browse'])
    self.btn_run.config(text=lang_data['btn_run'])

    # تحديث خيارات القائمة المنسدلة للصيغ
    combo_options = [
        lang_data['all_files'],
        lang_data['videos'],
        lang_data['images'],
        lang_data['texts'],
        lang_data['pdf'],
        lang_data['audio'],
        lang_data['archives'],
        lang_data['custom'],
    ]
    self.ext_combo['values'] = combo_options
    self.ext_combo.current(0)

  def on_ext_change(self, event):
    # مسح الحقل المخصص عند اختيار خيار محدد من القائمة
    if self.ext_combo.current() != 7:  # ليس الخيار المخصص
      self.custom_ext_entry.delete(0, tk.END)

  def select_source(self):
    dir_path = filedialog.askdirectory()
    if dir_path:
      self.src_entry.delete(0, tk.END)
      self.src_entry.insert(0, dir_path)

  def select_destination(self):
    dir_path = filedialog.askdirectory()
    if dir_path:
      self.dst_entry.delete(0, tk.END)
      self.dst_entry.insert(0, dir_path)

  def run_search(self):
    lang_data = LANGUAGES[self.current_lang]
    src = self.src_entry.get().strip()
    dst = self.dst_entry.get().strip()

    if not src or not dst:
      messagebox.showerror('Error', lang_data['err_fill'])
      return

    if not os.path.exists(src) or not os.path.exists(dst):
      messagebox.showerror('Error', lang_data['err_path'])
      return

    # تحديد الامتدادات المطلوبة للبحث
    selected_index = self.ext_combo.current()
    custom_ext = self.custom_ext_entry.get().strip().lower()

    target_extensions = []

    if custom_ext:  # إذا أدخل المستخدم امتداد مخصص
      if not custom_ext.startswith('.'):
        custom_ext = '.' + custom_ext
      target_extensions = [custom_ext]
    elif selected_index == 0:  # جميع الملفات
      target_extensions = []
    elif selected_index == 1:  # فيديو
      target_extensions = EXT_MAP['videos']
    elif selected_index == 2:  # صور
      target_extensions = EXT_MAP['images']
    elif selected_index == 3:  # نصية
      target_extensions = EXT_MAP['texts']
    elif selected_index == 4:  # PDF
      target_extensions = EXT_MAP['pdf']
    elif selected_index == 5:  # صوت
      target_extensions = EXT_MAP['audio']
    elif selected_index == 6:  # مضغوطة
      target_extensions = EXT_MAP['archives']

    count = 0
    try:
      # os.walk للبحث داخل المجلد والمجلدات الفرعية
      for root_dir, dirs, files in os.walk(src):
        for file in files:
          file_lower = file.lower()

          # التحقق من مطابقة الصيغة
          match = False
          if not target_extensions:  # جميع الملفات
            match = True
          else:
            for ext in target_extensions:
              if file_lower.endswith(ext):
                match = True
                break

          if match:
            src_file_path = os.path.join(root_dir, file)
            dst_file_path = os.path.join(dst, file)

            # تجنب استبدال ملف بآخر يحمل نفس الاسم
            if not os.path.exists(dst_file_path):
              shutil.copy2(src_file_path, dst_file_path)
              count += 1

      messagebox.showinfo('FileGatherer', lang_data['success'].format(count))
    except Exception as e:
      messagebox.showerror('Error', f"{lang_data['err_unknown']}\n{e}")


if __name__ == '__main__':
  root = tk.Tk()
  app = FileGathererApp(root)
  root.mainloop()
    

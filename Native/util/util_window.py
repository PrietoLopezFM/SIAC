def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    screen_width = ventana.winfo_screenwidth()
    screen_length = ventana.winfo_screenheight()
    x = int((screen_width/2) - (aplicacion_ancho/2))
    y = int((screen_length/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}")
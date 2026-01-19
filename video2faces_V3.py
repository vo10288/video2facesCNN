#
# 20260119H16:33 - Updated 2026
# 
## Frame salvati SENZA rettangoli verdi (default)

#python video2faces_v2.py -i video.mp4

# Frame salvati CON rettangoli verdi
#python video2faces_v2.py -i video.mp4 -t
#python video2faces_v2.py -i video.mp4 --tag
# by Visi@n
# LICENSE:
# THIS SCRIPT USE FACE_RECOGNITION LIBRARY [https://github.com/ageitgey/face_recognition/blob/master/LICENSE]
# THIS SCRIPT HAS BEEN MODIFIED BY Antonio 'Visi@n' Broi [antonio@tsurugi-linux.org] and it's licensed under the MIT License
#
# Example: video2faces.py -i video.mp4 -o ~/02.computer_vision/03.reports

import face_recognition
import cv2
from PIL import Image
from datetime import datetime
import argparse
import os
import html


def format_timestamp(seconds):
    """Converte i secondi in formato hh_mm_ss"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}_{minutes:02d}_{secs:02d}"


def format_timestamp_display(seconds):
    """Converte i secondi in formato hh:mm:ss per la visualizzazione"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def create_output_directories(base_output):
    """Crea le directory di output: volti e frame"""
    volti_dir = os.path.join(base_output, "volti")
    frame_dir = os.path.join(base_output, "frame")
    
    os.makedirs(volti_dir, exist_ok=True)
    os.makedirs(frame_dir, exist_ok=True)
    
    return volti_dir, frame_dir


def generate_html_report(report_data, output_dir, video_name):
    """Genera il report HTML con tutti i dati raccolti"""
    report_path = os.path.join(output_dir, "report.html")
    
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Estrazione Volti - {html.escape(video_name)}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            padding: 30px 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .stat-box {{
            background: rgba(255,255,255,0.1);
            padding: 15px 30px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #00d4ff;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #aaa;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}
        thead {{
            background: rgba(123, 44, 191, 0.3);
        }}
        th {{
            padding: 20px 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            vertical-align: middle;
        }}
        tr:hover {{
            background: rgba(255,255,255,0.05);
        }}
        .thumbnail {{
            width: 120px;
            height: auto;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .thumbnail:hover {{
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(0,212,255,0.3);
        }}
        .face-thumbnail {{
            width: 80px;
            height: auto;
            border-radius: 8px;
            border: 2px solid #7b2cbf;
        }}
        a {{
            color: #00d4ff;
            text-decoration: none;
            transition: color 0.3s;
        }}
        a:hover {{
            color: #7b2cbf;
        }}
        .time-badge {{
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .frame-badge {{
            background: rgba(255,255,255,0.1);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        .face-count {{
            background: #7b2cbf;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        footer {{
            text-align: center;
            padding: 30px;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
        .no-data {{
            text-align: center;
            padding: 50px;
            color: #666;
        }}
        @media (max-width: 768px) {{
            .thumbnail {{
                width: 80px;
            }}
            .face-thumbnail {{
                width: 60px;
            }}
            th, td {{
                padding: 10px 8px;
                font-size: 0.85em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎬 Report Estrazione Volti</h1>
            <p>Video: <strong>{html.escape(video_name)}</strong></p>
            <p>Generato il: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{len(report_data)}</div>
                    <div class="stat-label">Frame con volti</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{sum(item['face_count'] for item in report_data)}</div>
                    <div class="stat-label">Volti totali estratti</div>
                </div>
            </div>
        </header>
"""
    
    if report_data:
        html_content += """
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Timestamp</th>
                    <th>Frame</th>
                    <th>Volti</th>
                    <th>Anteprima Frame</th>
                    <th>Anteprime Volti</th>
                </tr>
            </thead>
            <tbody>
"""
        for idx, item in enumerate(report_data, 1):
            # Genera le anteprime dei volti
            face_previews = ""
            for face_file in item['face_files']:
                face_rel_path = os.path.join("volti", os.path.basename(face_file))
                face_previews += f'<a href="{face_rel_path}" target="_blank"><img src="{face_rel_path}" class="face-thumbnail thumbnail" alt="Volto"></a> '
            
            frame_rel_path = os.path.join("frame", os.path.basename(item['frame_file']))
            
            html_content += f"""
                <tr>
                    <td>{idx}</td>
                    <td><span class="time-badge">{item['timestamp_display']}</span></td>
                    <td><span class="frame-badge">Frame {item['frame_number']}</span></td>
                    <td><span class="face-count">{item['face_count']} volto/i</span></td>
                    <td><a href="{frame_rel_path}" target="_blank"><img src="{frame_rel_path}" class="thumbnail" alt="Frame {item['frame_number']}"></a></td>
                    <td>{face_previews}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
"""
    else:
        html_content += """
        <div class="no-data">
            <h2>Nessun volto rilevato nel video</h2>
            <p>Il sistema non ha trovato volti nei frame analizzati.</p>
        </div>
"""
    
    html_content += f"""
        <footer>
            <p>Generato con video2faces.py - Tsurugi Linux</p>
            <p><a href="https://tsurugi-linux.org" target="_blank">https://tsurugi-linux.org</a></p>
        </footer>
    </div>
</body>
</html>
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return report_path


def main():
    ap = argparse.ArgumentParser(
        description="Estrae volti da file video e genera un report HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s -i video.mp4
  %(prog)s -i video.mp4 -o ~/output_dir
  %(prog)s -i video.mp4 --skip-frames 5
  %(prog)s -i video.mp4 --model hog
        """
    )
    ap.add_argument("-i", "--input", required=True,
        help="File video di input")
    ap.add_argument("-o", "--output", default=None,
        help="Directory di output (default: timestamp corrente es. '2026_01_19_15_30_45')")
    ap.add_argument("--skip-frames", type=int, default=1,
        help="Processa 1 frame ogni N (default: 1, tutti i frame)")
    ap.add_argument("--model", choices=["cnn", "hog"], default="cnn",
        help="Modello per il rilevamento volti: 'cnn' (più accurato, GPU) o 'hog' (più veloce, CPU). Default: cnn")
    ap.add_argument("--upsample", type=int, default=1,
        help="Numero di upsampling per rilevare volti più piccoli (default: 1)")
    ap.add_argument("--no-display", action="store_true",
        help="Non mostrare la finestra video durante l'elaborazione")
    ap.add_argument("-t", "--tag", action="store_true",
        help="Disegna i rettangoli verdi sui volti nei frame salvati (default: no)")
    
    args = ap.parse_args()
    
    # Se non specificata, usa timestamp data/ora come nome directory
    if args.output is None:
        args.output = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    
    # Verifica che il file video esista
    if not os.path.isfile(args.input):
        print(f"Errore: Il file '{args.input}' non esiste.")
        return 1
    
    # Crea le directory di output
    base_output = args.output
    volti_dir, frame_dir = create_output_directories(base_output)
    
    print(f"Directory di output: {os.path.abspath(base_output)}")
    print(f"  - Volti: {volti_dir}")
    print(f"  - Frame: {frame_dir}")
    
    # Apri il video
    video_capture = cv2.VideoCapture(args.input)
    
    if not video_capture.isOpened():
        print(f"Errore: Impossibile aprire il video '{args.input}'")
        return 1
    
    # Ottieni informazioni sul video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    video_name = os.path.basename(args.input)
    
    print(f"\nVideo: {video_name}")
    print(f"FPS: {fps:.2f}")
    print(f"Frame totali: {total_frames}")
    print(f"Durata stimata: {format_timestamp_display(total_frames / fps)}")
    print(f"Modello: {args.model}")
    print(f"Skip frames: {args.skip_frames}")
    print("\nElaborazione in corso... (premi 'q' per interrompere)\n")
    
    # Variabili per il tracking
    report_data = []
    frame_count = 0
    faces_found_total = 0
    
    try:
        while True:
            ret, frame = video_capture.read()
            
            if not ret:
                break
            
            frame_count += 1
            
            # Skip frames se richiesto
            if frame_count % args.skip_frames != 0:
                continue
            
            # Calcola il timestamp corrente
            current_time_seconds = frame_count / fps
            timestamp_str = format_timestamp(current_time_seconds)
            timestamp_display = format_timestamp_display(current_time_seconds)
            
            # Rileva i volti
            face_locations = face_recognition.face_locations(
                frame, 
                number_of_times_to_upsample=args.upsample, 
                model=args.model
            )
            
            if face_locations:
                print(f"Frame {frame_count} ({timestamp_display}): trovati {len(face_locations)} volto/i")
                
                # Nome base per i file
                base_filename = f"{timestamp_str}_{frame_count:06d}"
                
                # Salva il frame intero
                frame_filename = f"{base_filename}.png"
                frame_path = os.path.join(frame_dir, frame_filename)
                
                # Prepara frame con rettangoli per visualizzazione
                frame_with_boxes = frame.copy()
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame_with_boxes, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Salva il frame (con o senza tag in base all'opzione)
                if args.tag:
                    cv2.imwrite(frame_path, frame_with_boxes)
                else:
                    cv2.imwrite(frame_path, frame)
                
                # Salva ogni volto
                face_files = []
                for face_idx, face_location in enumerate(face_locations):
                    top, right, bottom, left = face_location
                    
                    # Estrai il volto
                    face_image = frame[top:bottom, left:right]
                    
                    # Salva il volto
                    face_filename = f"{base_filename}_face{face_idx:02d}.png"
                    face_path = os.path.join(volti_dir, face_filename)
                    
                    pil_image = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
                    pil_image.save(face_path)
                    
                    face_files.append(face_path)
                    faces_found_total += 1
                
                # Aggiungi al report
                report_data.append({
                    'timestamp': timestamp_str,
                    'timestamp_display': timestamp_display,
                    'frame_number': frame_count,
                    'face_count': len(face_locations),
                    'frame_file': frame_path,
                    'face_files': face_files
                })
                
                # Mostra il frame se richiesto
                if not args.no_display:
                    cv2.imshow("Video - Face Detection", frame_with_boxes)
            
            else:
                # Mostra comunque il frame senza volti
                if not args.no_display:
                    cv2.imshow("Video - Face Detection", frame)
            
            # Progress
            if frame_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progresso: {progress:.1f}% ({frame_count}/{total_frames} frame)")
            
            # Controlla se l'utente vuole uscire
            if not args.no_display:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nInterrotto dall'utente.")
                    break
    
    except KeyboardInterrupt:
        print("\nInterrotto dall'utente (Ctrl+C).")
    
    finally:
        video_capture.release()
        cv2.destroyAllWindows()
    
    # Genera il report HTML
    print("\nGenerazione report HTML...")
    report_path = generate_html_report(report_data, base_output, video_name)
    
    # Statistiche finali
    print("\n" + "="*50)
    print("ELABORAZIONE COMPLETATA")
    print("="*50)
    print(f"Frame elaborati: {frame_count}")
    print(f"Frame con volti: {len(report_data)}")
    print(f"Volti totali estratti: {faces_found_total}")
    print(f"\nFile salvati in: {os.path.abspath(base_output)}")
    print(f"Report HTML: {report_path}")
    print("="*50)
    
    return 0


if __name__ == "__main__":
    exit(main())

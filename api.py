from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Metodo POST per popolare le tabelle dal file JSON
@app.route('/popola_tabelle', methods=['POST'])
def popola_tabelle():
    try:
        data = request.get_json()  # Ottieni i dati JSON dalla richiesta POST
        
        db_config = data.get("db_config", {})  # Ottieni i dettagli di connessione al database dal JSON
        gruppo = data.get("gruppo", {})  # Ottieni le informazioni del gruppo dal JSON
        uomini = data.get("uomini", [])  # Ottieni la lista degli uomini dal JSON
        donne = data.get("donne", [])  # Ottieni la lista delle donne dal JSON
        
        # Configura la connessione al database
        db = psycopg2.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )

        cursor = db.cursor()

        # Popola la tabella "Gruppi" e ottieni l'ID generato automaticamente
        query = "INSERT INTO Gruppi (data_visita, ora_inizio_visita, componenti_gruppo, gruppi_presenti) VALUES (%s, %s, %s, %s) RETURNING id_gruppo"
        values = (gruppo["data_visita"], gruppo["ora_inizio_visita"], gruppo["componenti_gruppo"], gruppo["gruppi_presenti"])
        cursor.execute(query, values)
        id_gruppo = cursor.fetchone()[0]  # Ottieni l'ID generato per il gruppo appena inserito
        
        # Popola la tabella "Uomini"
        for uomo in uomini:
            uomo["id_gruppo"] = id_gruppo  # Assegna l'ID del gruppo generato
            query = "INSERT INTO Uomini (id_gruppo, numero_bambini, numero_adolescenti, numero_adulti, numero_anziani, numero_disabilita_motorie, numero_disabilita_visive, numero_disabilita_cognitive, numero_disabilita_uditive_lis, numero_disabilita_uditive_sottotitoli, numero_italiani, numero_inglesi, numero_tedeschi, numero_spagnoli, numero_indiani, numero_giapponesi, numero_francesi, numero_cinesi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (uomo["id_gruppo"], uomo["numero_bambini"], uomo["numero_adolescenti"], uomo["numero_adulti"], uomo["numero_anziani"], uomo["numero_disabilita_motorie"], uomo["numero_disabilita_visive"], uomo["numero_disabilita_cognitive"], uomo["numero_disabilita_uditive_lis"], uomo["numero_disabilita_uditive_sottotitoli"], uomo["numero_italiani"], uomo["numero_inglesi"], uomo["numero_tedeschi"], uomo["numero_spagnoli"], uomo["numero_indiani"], uomo["numero_giapponesi"], uomo["numero_francesi"], uomo["numero_cinesi"] )
            cursor.execute(query, values)
        
        # Popola la tabella "Donne"
        for donna in donne:
            donna["id_gruppo"] = id_gruppo  # Assegna l'ID del gruppo generato
            query = "INSERT INTO Donne (id_gruppo, numero_bambine, numero_adolescenti, numero_adulte, numero_anziane, numero_disabilita_motorie, numero_disabilita_visive, numero_disabilita_cognitive, numero_disabilita_uditive_lis, numero_disabilita_uditive_sottotitoli, numero_italiane, numero_inglesi, numero_tedesche, numero_spagnole, numero_indiane, numero_giapponesi, numero_francesi, numero_cinesi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (donna["id_gruppo"], donna["numero_bambine"], donna["numero_adolescenti"], donna["numero_adulte"], donna["numero_anziane"], donna["numero_disabilita_motorie"], donna["numero_disabilita_visive"], donna["numero_disabilita_cognitive"], donna["numero_disabilita_uditive_lis"], donna["numero_disabilita_uditive_sottotitoli"], donna["numero_italiane"], donna["numero_inglesi"], donna["numero_tedesche"], donna["numero_spagnole"], donna["numero_indiane"], donna["numero_giapponesi"], donna["numero_francesi"], donna["numero_cinesi"])
            cursor.execute(query, values)

        db.commit()
        cursor.close()
        return jsonify({"message": "Tabelle popolate con successo."}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:34:07 2024

@author: francescatorazzi
"""

#Spotify feature generale 
#questo è perfetto 
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Inserisci le tue credenziali Spotify
#le trovi sulla dashboard di spotify for developers 
client_id = 'your client_id'
client_secret = 'your client_secret'

# Imposta le credenziali del client Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Carica il foglio Excel su cui ci sono i dati 
df = pd.read_excel("excel sheet where you have at least two columns one with the track name and one with the artist name")

# Lista per salvare i dati delle tracce
tracks_data = []

# Itera sul dataframe per ottenere le informazioni delle tracce
for index, row in df.iterrows():
    # Ottieni il nome dell'artista e il nome della traccia
    artist_name = row['﻿artist_name']
    track_name = row['﻿track_name']
    
    # Cerca la traccia su Spotify
    results = sp.search(q=f'artist:{artist_name} track:{track_name}', type='track')
    
    # Verifica se sono stati trovati risultati
    if results['tracks']['items']:
        track_info = results['tracks']['items'][0]
        
        # Ottieni l'URI della traccia
        track_uri = track_info['uri']
        
        # Ottieni tutte le informazioni disponibili sulla traccia
        track_full_info = sp.track(track_uri)
        track_audio_features = sp.audio_features(track_uri)[0]
        
        # Salva le informazioni della traccia
        tracks_data.append({
            'endTime': row['endTime'],
            'artist_name': artist_name,
            'track_name': track_name,
            'msPlayed': row['msPlayed'],
            'track_uri': track_uri,
            # Informazioni di base della traccia
            'track_duration_ms': track_full_info['duration_ms'],
            'track_popularity': track_full_info['popularity'],
            # Caratteristiche audio della traccia
            'acousticness': track_audio_features['acousticness'],
            'danceability': track_audio_features['danceability'],
            'energy': track_audio_features['energy'],
            'instrumentalness': track_audio_features['instrumentalness'],
            'key': track_audio_features['key'],
            'liveness': track_audio_features['liveness'],
            'loudness': track_audio_features['loudness'],
            'mode': track_audio_features['mode'],
            'speechiness': track_audio_features['speechiness'],
            'tempo': track_audio_features['tempo'],
            'time_signature': track_audio_features['time_signature'],
            'valence': track_audio_features['valence']
        })
    else:
        # Se la traccia non è stata trovata, inserisci valori vuoti
        tracks_data.append({
            'endTime': row['endTime'],
            'artist_name': artist_name,
            'track_name': track_name,
            'msPlayed': row['msPlayed'],
            'track_uri': None,
            # Inserisci valori vuoti per tutte le caratteristiche audio
            'track_duration_ms': None,
            'track_popularity': None,
            'acousticness': None,
            'danceability': None,
            'energy': None,
            'instrumentalness': None,
            'key': None,
            'liveness': None,
            'loudness': None,
            'mode': None,
            'speechiness': None,
            'tempo': None,
            'time_signature': None,
            'valence': None
        })

# Converti i dati delle tracce in un DataFrame
tracks_df = pd.DataFrame(tracks_data)

# Salva il DataFrame in un nuovo foglio Excel
tracks_df.to_excel('new excel file', index=False)

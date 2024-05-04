using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;


public class PlatformGenerator : MonoBehaviour
{
    public Tilemap tilemap;
    public TileBase platformTile; // Tipo de plataforma
    public int platformWidth = 1;
    public float[] heights;
    public float minHorizontalSpacing = 0f;
    public float maxHorizontalSpacing = 0.1f;
    public float generationOffset = 10f; // Distancia desde la cámara para comenzar a generar
    public float generationFrequency;  // Frecuencia de generación de plataformas (segundos por plataforma)

    private int currentGenerationIndex = 0;
    private float timer = 0f;
    private Vector3Int lastTilePosition;

    void Start()
    {
        lastTilePosition = tilemap.origin;

        ModelRunner.OnModelReady += StartGeneration;
    }

    void StartGeneration()
    {
        // Iniciar la generación de plataformas aquí
        Debug.Log("Iniciando generación de plataformas...");
    }

    void Update()
    {
        // Incrementar el temporizador
        timer += Time.deltaTime;

        // Verificar si es necesario generar más plataformas
        if (timer >= generationFrequency)
        {
            GeneratePlatform();

            // Reiniciar el temporizador
            timer = 0f;
        }
    }

    void GeneratePlatform()
    {
        // Calcula las posiciones de la nueva plataforma
        float horizontalOffset = Random.Range(minHorizontalSpacing, maxHorizontalSpacing);
        Vector3Int newTilePosition = lastTilePosition + new Vector3Int(platformWidth + Mathf.RoundToInt(horizontalOffset), Mathf.RoundToInt(heights[currentGenerationIndex]), 0);

        // Coloca el Tile en la posición calculada
        tilemap.SetTile(newTilePosition, platformTile);

        // Actualiza la posición de la última plataforma generada
        lastTilePosition = newTilePosition;

        // Incrementa el índice de generación para la próxima plataforma
        currentGenerationIndex++;
        if (currentGenerationIndex >= heights.Length)
        {
            currentGenerationIndex = 0; // Vuelve al inicio del array si se alcanza el final
        }
    }

    void OnDestroy()
    {
        ModelRunner.OnModelReady -= StartGeneration;
    }
}
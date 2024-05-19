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
    public float minHorizontalSpacing = 0.5f;
    public float maxHorizontalSpacing = 2.5f;
    public float generationFrequency;  // Frecuencia de generación de plataformas (segundos por plataforma)

    private int currentGenerationIndex = 0;
    private Vector3Int lastTilePosition;

    void Start()
    {
        lastTilePosition = FindLastTilePosition();

        ModelRunner.OnModelReady += StartGeneration;
    }

    void StartGeneration()
    {
        Debug.Log("Iniciando generación de plataformas...");

        // Iniciar la generación de plataformas
        InvokeRepeating("GeneratePlatform", 0f, generationFrequency);
    }

    void GeneratePlatform()
    {
        // Calcula las posiciones de la nueva plataforma
        float horizontalOffset = Random.Range(minHorizontalSpacing, maxHorizontalSpacing);
        Vector3Int newTilePosition = new Vector3Int(lastTilePosition.x + platformWidth + Mathf.RoundToInt(horizontalOffset), Mathf.RoundToInt(heights[currentGenerationIndex]), 0);

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

    Vector3Int FindLastTilePosition()
    {
        Vector3Int lastPosition = tilemap.origin;
        foreach (var pos in tilemap.cellBounds.allPositionsWithin)
        {
            if (tilemap.HasTile(pos))
            {
                if (pos.x > lastPosition.x)
                {
                    lastPosition = pos;
                }
            }
        }
        return lastPosition;
    }

    void OnDestroy()
    {
        ModelRunner.OnModelReady -= StartGeneration;
    }
}
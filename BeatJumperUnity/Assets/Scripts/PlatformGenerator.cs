using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;


public class PlatformGenerator : MonoBehaviour
{
    public Tilemap tilemap;
    public TileBase[] platformTiles;
    
    public int platformWidth = 1;
    public float minVerticalSpacing = 0f;
    public float maxVerticalSpacing = 0.1f;
    public float minHorizontalSpacing = 0f;
    public float maxHorizontalSpacing = 0.1f;
    public float generationOffset = 10f; // Distancia desde la cámara para comenzar a generar

    private Vector3Int lastTilePosition;

    void Start()
    {
        lastTilePosition = tilemap.origin;
    }

    void Update()
    {
        // Verifica si es necesario generar más plataformas
        Vector3 cameraPosition = Camera.main.transform.position;
        if (cameraPosition.x >= lastTilePosition.x - generationOffset)
        {
            GeneratePlatform();
        }
    }

    void GeneratePlatform()
    {
        // Selecciona un Tile aleatorio para la plataforma
        TileBase randomTile = platformTiles[Random.Range(0, platformTiles.Length)];

        // Calcula las posiciones de la nueva plataforma
        float verticalOffset = Random.Range(minVerticalSpacing, maxVerticalSpacing);
        if (Random.value < 0.5f) // Genera algunas plataformas arriba y otras abajo
        {
            verticalOffset = -verticalOffset;
        }
        float horizontalOffset = Random.Range(minHorizontalSpacing, maxHorizontalSpacing);
        Vector3Int newTilePosition = lastTilePosition + new Vector3Int(platformWidth + Mathf.RoundToInt(horizontalOffset), Mathf.RoundToInt(verticalOffset), 0);

        // Coloca el Tile en la posición calculada
        tilemap.SetTile(newTilePosition, randomTile);

        // Actualiza la posición de la última plataforma generada
        lastTilePosition = newTilePosition;
    }
}
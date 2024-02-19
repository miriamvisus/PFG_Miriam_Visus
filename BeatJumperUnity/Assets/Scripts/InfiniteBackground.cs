using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InfiniteBackground : MonoBehaviour
{
    public GameObject backgroundPrefab; // Prefab del fondo que se duplicará
    public float spawnOffset = 10f; // Distancia entre cada copia del fondo
    public int initialBackgrounds = 3; // Número inicial de fondos

    private Camera mainCamera;
    private Transform lastBackground; // Último fondo generado
    private float lastCameraX; // Posición X de la cámara en el fotograma anterior

    void Start()
    {
        mainCamera = Camera.main;
        lastCameraX = mainCamera.transform.position.x;

        // Genera los fondos iniciales
        GenerateInitialBackgrounds();
    }

    void Update()
    {
        // Calcula el desplazamiento horizontal de la cámara
        float cameraDeltaX = mainCamera.transform.position.x - lastCameraX;

        // Si la cámara se ha movido lo suficiente, genera un nuevo fondo
        if (Mathf.Abs(cameraDeltaX) >= spawnOffset)
        {
            GenerateBackground();
            lastCameraX = mainCamera.transform.position.x;
        }
    }

    void GenerateInitialBackgrounds()
    {
        // Genera un número inicial de fondos
        for (int i = 0; i < initialBackgrounds; i++)
        {
            GenerateBackground();
        }
    }

    void GenerateBackground()
    {
        // Instancia un nuevo fondo
        GameObject newBackground = Instantiate(backgroundPrefab, transform);

        // Posiciona el nuevo fondo al lado del último fondo generado
        if (lastBackground != null)
        {
            Vector3 newPosition = lastBackground.position + Vector3.right * spawnOffset;
            newBackground.transform.position = newPosition;
        }

        // Actualiza el último fondo generado
        lastBackground = newBackground.transform;
    }
}
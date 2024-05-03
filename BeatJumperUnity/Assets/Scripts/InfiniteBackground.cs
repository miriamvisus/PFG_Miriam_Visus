using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class InfiniteBackground : MonoBehaviour
{
    public bool scrollHorizontally = true;
    public bool scrollVertically = false;

    private Camera mainCamera;
    private Vector3 lastCameraPosition;
    private Vector3 deltaCameraPosition;

    private void Start()
    {
        mainCamera = Camera.main;
        lastCameraPosition = mainCamera.transform.position;
    }

    private void Update()
    {
        // Calcula el cambio en la posición de la cámara desde el último frame
        deltaCameraPosition = mainCamera.transform.position - lastCameraPosition;

        // Guarda la posición actual de la cámara para el próximo frame
        lastCameraPosition = mainCamera.transform.position;

        // Aplica el mismo cambio de posición a este objeto
        if (scrollHorizontally)
        {
            transform.position += new Vector3(deltaCameraPosition.x, 0, 0);
        }

        if (scrollVertically)
        {
            transform.position += new Vector3(0, deltaCameraPosition.y, 0);
        }
    }
}


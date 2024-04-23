using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FallDetectorMovement : MonoBehaviour
{
    private Camera mainCamera;
    private Vector3 lastCameraPosition;

    void Start()
    {
        mainCamera = Camera.main; 
        lastCameraPosition = mainCamera.transform.position;
    }

    void Update()
    {
        Vector3 currentCameraPosition = mainCamera.transform.position;
        float cameraSpeed = (currentCameraPosition - lastCameraPosition).magnitude / Time.deltaTime;
        transform.Translate(Vector3.right * cameraSpeed * Time.deltaTime);
        lastCameraPosition = currentCameraPosition;
        if (transform.position.x > Screen.width)
        {
            ResetPositionToLeft();
        }
    }

    void ResetPositionToLeft()
    {
        transform.position = new Vector3(0, transform.position.y, transform.position.z);
    }
}
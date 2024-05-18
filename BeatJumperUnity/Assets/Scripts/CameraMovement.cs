using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class CameraMovement : MonoBehaviour
{
    public GameObject Bunny;
   
    void Update()
    {
        Vector3 position = transform.position;
        position.x = Bunny.transform.position.x;
        transform.position = position;
    }
}
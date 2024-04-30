using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class CameraScript : MonoBehaviour
{
    public GameObject bunny;
   
    void Update()
    {
        Vector3 position = transform.position;
        position.x = bunny.transform.position.x;
        transform.position = position;
    }
}
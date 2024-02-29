using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AdaptationController : MonoBehaviour
{
    public CharacterController characterController;
    
    public float baseSpeed = 5f; // cambiar por la velocidad del personaje
    private float currentSpeed;

    public GameObject obstaclePrefab;
    public Transform obstacleSpawnPoint;
    public float baseObstacleFrequency = 2f;
    private float currentObstacleFrequency;

    void AdjustCharacterSpeed(float musicTempo)
    {
        currentSpeed = baseSpeed + musicTempo * 0.5f; 
    }


    void AdjustObstacleFrequency(float musicEnergy)
    {
        currentObstacleFrequency = baseObstacleFrequency / (1 + musicEnergy); 
    }

    void SpawnObstacle()
    {
        Instantiate(obstaclePrefab, obstacleSpawnPoint.position, Quaternion.identity);
    }

    public void UpdateAdaptation(float musicTempo, float musicEnergy)
    {
        AdjustCharacterSpeed(musicTempo);

        AdjustObstacleFrequency(musicEnergy);

        // Lógica adicional de adaptación, como cambiar la apariencia del entorno o la música de fondo, según sea necesario

        if (Random.value < currentObstacleFrequency * Time.deltaTime)
        {
            SpawnObstacle();
        }
    }
}

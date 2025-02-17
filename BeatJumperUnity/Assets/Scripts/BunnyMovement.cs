using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class BunnyMovement : MonoBehaviour
{
    public float Speed;
    public float JumpForce;

    private Rigidbody2D Rigidbody2D;
    private Animator Animator;
    private bool Grounded;
    private bool IsModelReady;

    void Start()
    {
        Rigidbody2D = GetComponent<Rigidbody2D>();
        Animator = GetComponent<Animator>();

        ModelRunner.OnModelReady += StartMovement;
    }

    void Update()
    {
        if (!IsModelReady) return;

        // Movimiento horizontal continuo
        transform.Translate(Vector2.right * Speed * Time.deltaTime);

        // Verifica la entrada para el salto
        if ((Input.GetKeyDown(KeyCode.W) || Input.GetKeyDown(KeyCode.UpArrow)))
        {
            Jump();
        }

        // Actualización de la animación
        Animator.SetBool("Running", true);
        Animator.SetBool("Jumping", !Grounded);
    }

    void StartMovement()
    {
        Debug.Log("Iniciando movimiento del personaje...");
        IsModelReady = true;
    }

    private void Jump()
    {
        // Verifica si está en el suelo antes de saltar
        if (Grounded)
        {
            Rigidbody2D.AddForce(Vector2.up * JumpForce);
        }
    }
    
    private void FixedUpdate() 
    {
        Grounded = Physics2D.Raycast(transform.position, Vector2.down, 2.0f);
    }

    void OnTriggerEnter2D(Collider2D FallDetectorCollider)
    {
        if (FallDetectorCollider.gameObject.CompareTag("FallDetector"))
        {
            Debug.Log("Te has caído.");
            Animator.SetBool("Hurting", true);
            
            // Detener la generación de plataformas
            GameObject platformManager = GameObject.Find("PlatformManager");
            if (platformManager != null)
            {
                PlatformGenerator platformGenerator = platformManager.GetComponent<PlatformGenerator>();
                if (platformGenerator != null)
                {
                    platformGenerator.StopGeneration();
                }
            }

            SceneManager.LoadScene("GameOverScene");
        }
    }

    void OnDestroy()
    {
        ModelRunner.OnModelReady -= StartMovement;
    }
}
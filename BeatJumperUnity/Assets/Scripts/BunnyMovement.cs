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

    void Start()
    {
        Rigidbody2D = GetComponent<Rigidbody2D>();
        Animator = GetComponent<Animator>();

        ModelRunner.OnModelReady += StartMovement;
    }

    void StartMovement()
    {
        // Iniciar el movimiento del personaje aquí
        Debug.Log("Iniciando movimiento del personaje...");
    }

    void Update()
    {
        transform.Translate(Vector2.right * Speed * Time.deltaTime);

        if (Input.GetKeyDown(KeyCode.W) || Input.GetKeyDown(KeyCode.UpArrow))
        {
            Jump();
        }

        // Actualización de la animación
        Animator.SetBool("Running", true);
        Animator.SetBool("Jumping", !Grounded);
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

    public void OnTriggerEnter2D(Collider2D FallDetectorCollider)
    {
        if (FallDetectorCollider.gameObject.CompareTag("FallDetector"))
        {
            Animator.SetBool("Hurting", true);
            Invoke("EndGameWithDelay", 0.3f);
        }
    }

    private void EndGameWithDelay()
    {
        Debug.Log("El juego ha terminado.");
        SceneManager.LoadScene("GameOverScene");
    }

    void OnDestroy()
    {
        ModelRunner.OnModelReady -= StartMovement;
    }
}
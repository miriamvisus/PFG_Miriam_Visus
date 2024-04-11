using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class GameManager
{
    public static void EndGame()
    {
        Debug.Log("El juego ha terminado.");
        SceneManager.LoadScene("GameOverScene");
    }
}
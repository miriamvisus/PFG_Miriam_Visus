using UnityEngine;


public class UnityMainThreadDispatcher : MonoBehaviour
{
    private static UnityMainThreadDispatcher instance;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public static void ExecuteOnMainThread(System.Action action)
    {
        if (instance != null)
        {
            instance.Execute(action);
        }
    }

    private void Execute(System.Action action)
    {
        if (action != null)
        {
            action();
        }
    }
}
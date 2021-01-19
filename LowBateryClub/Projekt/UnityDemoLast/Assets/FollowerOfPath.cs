using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using PathCreation;

public class FollowerOfPath : MonoBehaviour
{
    public PathCreator pathCreator;
    public float speed = 10;
    float distanceTravelled;
    private GameObject carObject;
    private float targetTimeout = 7.0f;

    // Start is called before the first frame update
    void Start()
    {
        carObject = GameObject.Find("Car");
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.time > targetTimeout)
        {
            distanceTravelled += speed * Time.deltaTime;
            transform.position = pathCreator.path.GetPointAtDistance(distanceTravelled);

            Vector3 targetPostition = new Vector3(carObject.transform.position.x, this.transform.position.y, carObject.transform.position.z);
            this.transform.LookAt(targetPostition);

        }
    }
}

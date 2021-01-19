using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AirSimUnity {
    public class TrailColors : MonoBehaviour
    {
        private TrailRenderer trail;

        private GameObject gameObject;
        private Car car;
        private double speed;
        private double prevSpeed = 0.0f;

        // Start is called before the first frame update
        void Start()
        {
            gameObject = GameObject.Find("Car");
            car = GetComponent<Car>();
            
            trail = GetComponent<TrailRenderer>();
            trail.endColor = Color.black;
            trail.startColor = Color.black;
        }

        // Update is called once per frame
        void Update()
        {
            //Pridobljena hitrost
            speed = car.carData.speed;

            if(speed < 0.1f){
                trail.endColor = Color.blue;
                trail.startColor = Color.blue;
            }else{

                if(speed < prevSpeed - 0.1f && speed > prevSpeed + 0.1f){
                    trail.endColor = Color.green;
                    trail.startColor = Color.green;
                }else if(speed > prevSpeed + 0.5f){
                    trail.endColor = Color.yellow;
                    trail.startColor = Color.yellow;
                }else if(speed < prevSpeed - 0.5f){
                    trail.startColor = Color.red;
                    trail.endColor = Color.red;
                }

            }
            //Debug.Log(speed);
            //Change width of trail on speed.
            if(speed < 1.0f){
                trail.endWidth = 0.2f;
                trail.startWidth = 0.2f;
            }else if(speed > 10 && speed < 30){
                trail.endWidth = 0.5f;
                trail.startWidth = 0.5f;
            }else if(speed > 30 && speed < 40){
                trail.endWidth = 1.0f;
                trail.startWidth = 1.0f;
            }else if(speed > 40){
                trail.endWidth = 3.0f;
                trail.startWidth = 3.0f;
            }




            prevSpeed = speed;

        }
    }

}

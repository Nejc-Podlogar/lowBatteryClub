using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace AirSimUnity
{

    public class IzpisAvto : MonoBehaviour
    {
        // Start is called before the first frame update
        public Text TextSpeed;
        //public Text TextSteering;
        //public Text TextThrottle;
        //public Text TextFootBreak;
        //public Text TextHandBreak;

        public GameObject TextSteering;
        public GameObject TextThrottle;
        public GameObject TextFootBreak;
        public GameObject TextHandBreak;

        //public GameObject TextSteering;
        private GameObject carObj;
        private Car car;
        void Start()
        {
            carObj = GameObject.Find("Car");
            car = carObj.GetComponent<Car>();

            TextSpeed = GetComponent<Text>();

            TextSteering = GameObject.Find("TextSteering");
            TextThrottle = GameObject.Find("TextThrottle");
            TextFootBreak = GameObject.Find("TextFootBreak");
            TextHandBreak = GameObject.Find("TextHandBreak");

            //TextSteering = GetComponent<Text>();
            //TextThrottle = GetComponent<Text>();
            //TextFootBreak = GetComponent<Text>();
            //TextHandBreak = GetComponent<Text>();


            //TextSpeed.text = "Spremenjeno iz skripte";

            //TextSteering = GameObject.Find("TextSteering");

            //TextSteering.GetComponent<Text>().text = "Ponovno iz skripte..pls work";
        }

        // Update is called once per frame
        void Update()
        {
            TextSpeed.GetComponent<Text>().text = "Hitrost: " + car.getCarData().speed;
            TextSteering.GetComponent<Text>().text = "Zavijanje: " + car.getSteering();
            TextThrottle.GetComponent<Text>().text = "Plin: " + car.getThrottle();
            TextFootBreak.GetComponent<Text>().text = "Zaviranje: " + car.getFootBreak();
            TextHandBreak.GetComponent<Text>().text = "Roèna: " + car.getHandBrake();

            
            //TextThrottle.text = "Throttle: " + car.getThrottle();
            //TextFootBreak.text = "Foot break: " + car.getFootBreak();
            //TextHandBreak.text = "Hand break: " + car.getHandBrake();
        }
    }

}


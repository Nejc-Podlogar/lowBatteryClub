using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

namespace AirSimUnity
{

    public class PodatkiAvto : MonoBehaviour
    {
        // Start is called before the first frame update
        private GameObject carObject;
        // private Vehicle vehicle;
        private Car car;
        float prevY, curY, prevX, curX, prevZ, curZ;

        public GameObject TextSpeed2;
        public GameObject TextSteering2;
        public GameObject TextThrottle2;
        public GameObject TextFootBreak2;
        public GameObject TextHandBreak2;

        void Start()
        {
            carObject = GameObject.Find("Car");
            //vehicle = GetComponent<Vehicle>();
            //Debug.Log(vehicle.isApiEnabled);
            car = carObject.GetComponent<Car>();

            prevX = car.transform.eulerAngles.x;
            prevY = car.transform.eulerAngles.y;
            prevZ = car.transform.eulerAngles.z;

            TextSpeed2 = GameObject.Find("TextSpeed2");
            TextSteering2 = GameObject.Find("TextSteering2");
            TextThrottle2 = GameObject.Find("TextThrottle2");
            TextFootBreak2 = GameObject.Find("TextFootBreak2");
            TextHandBreak2 = GameObject.Find("TextHandBreak2");
            //this.transform.Rotate(20, 0, 0, Space.Self);
        }

        // Update is called once per frame
        void Update()
        {
            //this.transform.position = Camera.main.transform.position + Camera.main.transform.forward * 10;
            //this.transform.position = this.transform.parent.position + Vector3.left;


            //this.transform.position += new Vector3(car.transform.eulerAngles.y, 0, 0);

            curY = car.transform.eulerAngles.y;

            //Vector3 targetPosition = new Vector3(carObject.transform.position.x - 4, carObject.transform.position.y + 2, carObject.transform.position.z);
            //this.transform.InverseTransformPoint(targetPosition);
            this.transform.position = carObject.transform.position + carObject.transform.right * -4;
            this.transform.position += new Vector3(0, 2, 0);
            
            this.transform.Rotate(0, curY - prevY, 0, Space.Self);

            prevY = curY;
            prevX = curX;
            prevZ = curZ;


            TextSpeed2.GetComponent<Text>().text = "Hitrost: " + car.getCarData().speed;
            TextSteering2.GetComponent<Text>().text = "Zavijanje: " + Decimal.Round((decimal)car.getSteering(), 3);
            TextThrottle2.GetComponent<Text>().text = "Plin: " + Decimal.Round((decimal)car.getThrottle(), 3);
            TextFootBreak2.GetComponent<Text>().text = "Zaviranje: " + Decimal.Round((decimal)car.getFootBreak(), 3);
            TextHandBreak2.GetComponent<Text>().text = "Plin: " + Decimal.Round((decimal)car.getHandBrake(), 3);
        }
    }
}
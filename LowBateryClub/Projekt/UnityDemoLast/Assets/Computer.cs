
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AirSimUnity
{
    public class Computer : MonoBehaviour
    {
        private GameObject carObject;
        // private Vehicle vehicle;
        private Car car;
        // Start is called before the first frame update

        float prevY, curY;

        void Start()
        {
            //vehicle.isApiEnabled;

            carObject = GameObject.Find("Car");
            //vehicle = GetComponent<Vehicle>();
            //Debug.Log(vehicle.isApiEnabled);
            car = carObject.GetComponent<Car>();

            prevY = car.transform.eulerAngles.y;

            this.transform.Rotate(0, 45, 0, Space.Self);
        }

        // Update is called once per frameS
        void Update()
        {

            //Debug.Log(car.isApiEnabled);
            if (car.getApiEnabled())
            {
                Vector3 targetPosition = new Vector3(carObject.transform.position.x, carObject.transform.position.y + 2, carObject.transform.position.z);
                this.transform.position = targetPosition;

                curY = car.transform.eulerAngles.y;

                this.transform.Rotate(0, curY - prevY, 0, Space.Self);

                prevY = curY;

                //Vector3 l = new Vector3(carObject.transform.position.x, carObject.transform.position.y + 2, carObject.transform.position.z + 20);
                //this.transform.LookAt(l);
            }
            else
            {
                this.enabled = false;
            }
        }
    }
}
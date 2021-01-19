using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace AirSimUnity
{
    public class Target : MonoBehaviour
    {
        /*private GameObject carObject;
        public PathToFollow pathToFollow;
        public int currWaypoint = 0;
        public float speed;
       // private float currDistance 1.0f;
        public float rotationSpeed = 5.0f;
        public string pathName;
        private Vector3 lastPosition;
        private Vector3 currPosition;*/

        // Start is called before the first frame update
        void Start()
        {
            /*carObject = GameObject.Find("Car");
            pathToFollow = GameObject.Find(pathName).GetComponent<PathToFollow>();
            lastPosition = transform.position;*/
        }

        // Update is called once per frame
        void Update()
        {
            /*float distance = Vector3.Distance(pathToFollow.pathObj[currWaypoint].position, transform.position);
            transform.position = Vector3.MoveTowards(transform.position, pathToFollow.pathObj[currWaypoint].position, Time.deltaTime * speed);


            // turn towards car object
            Vector3 targetPostition = new Vector3(carObject.transform.position.x, this.transform.position.y, carObject.transform.position.z);
            this.transform.LookAt(targetPostition);*/
        }
    }
}

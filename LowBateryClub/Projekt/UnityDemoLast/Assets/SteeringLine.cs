using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace AirSimUnity
{
    public class SteeringLine : MonoBehaviour
    {
        private GameObject carObject;
        private Car car;
        private GameObject targetObject;
        public string levoDesno;
        private GameObject leftRightObj;

        // Start is called before the first frame update
        void Start()
        {
            carObject = GameObject.Find("Car");
            car = carObject.GetComponent<Car>();
            targetObject = GameObject.Find("Target");
            leftRightObj = GameObject.Find("TextLevoDesno");
            //Create a line renderer object
            LineRenderer lineRenderer = gameObject.AddComponent<LineRenderer>();
            lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
            lineRenderer.widthMultiplier = 2;
            lineRenderer.positionCount = 2;

            // A simple 2 color gradient with a fixed alpha of 1.0f.
            float alpha = 1.0f;
            Gradient gradient = new Gradient();
            gradient.SetKeys(
                new GradientColorKey[] { new GradientColorKey(Color.green, 0.0f), new GradientColorKey(Color.green, 1.0f) },
                new GradientAlphaKey[] { new GradientAlphaKey(alpha, 0.0f), new GradientAlphaKey(alpha, 1.0f) }
            );
            lineRenderer.colorGradient = gradient;
            lineRenderer.useWorldSpace = false;
        }

        // Update is called once per frame
        void Update()
        {
            //set position of points in the line
            LineRenderer lineRenderer = GetComponent<LineRenderer>();
            lineRenderer.SetPosition(0, new Vector3(0, 0.5f, 2));
            //2nd point is 10 units away from the car, car.steering determines where the line will face(laft/right)
            lineRenderer.SetPosition(1, new Vector3(car.steering, 0.5f, 10));

            Vector3 heading = targetObject.transform.position - transform.position;
            levoDesno = checkLevoDesno(transform.forward, heading, transform.up);

            //Debug.Log("target " + levoDesno);
            leftRightObj.GetComponent<Text>().text = levoDesno;
        }

        string checkLevoDesno(Vector3 fwd, Vector3 targetDir, Vector3 up)
        {
            Vector3 perp = Vector3.Cross(fwd, targetDir);
            float dir = Vector3.Dot(perp, up);

            if (dir > 1.0f)
            {
                return "Tarca desno";
            }
            else if (dir < -1.0f)
            {
                return "Tarca levo";
            }
            else
            {
                return "Tarca spredaj";
            }
        }
    }
}

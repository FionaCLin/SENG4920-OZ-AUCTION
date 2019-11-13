import aws from "aws-sdk";
//import secret from "./awsconfig.json";

export function uploadImage(file, done) {
  //const s3 = new aws.S3(secret);
  const s3 = new aws.S3();

  s3.upload(
    {
      Bucket: "seng4920album",
      Key: `${Date.now()}-${file.name}`,
      Body: file,
      ACL: "public-read"
    },
    (err, res) => {
      console.log(err, res);
      done(err, res);
    }
  );
}

from app_factory import create_app
import scripts.get_credentials_from_s3

app = create_app()
scripts.get_credentials_from_s3.main()

if __name__ == "__main__":

    app.run(
        debug=True, port=5001
    )


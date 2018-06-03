# py-natwest
Command-line access to Natwest Online Banking account

#### Docker
```bash
docker build -t natwest_zoom:latest .
docker run -it --rm -v $(pwd)/config:/opt/natwest/config natwest_zoom:latest ./natwest force
docker run -it --rm -v $(pwd)/config:/opt/natwest/config natwest_zoom:latest
```

#### Cron Jobs
```
0 9     * * *   martin    docker run -i --rm -v /etc/natwest:/opt/natwest/config natwest_zoom:latest ./natwest force >/dev/null 2>&1 || true
*/1 *	  * * *   martin    docker run -i --rm -v /etc/natwest:/opt/natwest/config natwest_zoom:latest >/dev/null 2>&1 || true
```

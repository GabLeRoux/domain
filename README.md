# Domain enumall

[Recon-ng][recon-ng] and [altdns][altdns] are awesome. This script combines the power of these tools with the ability to run multiple domains within the same session.

TLDR; I just want to do my subdomain discovery via ONE command and be done with it.

Only 1 module needs an api key: `/api/google_site`. Find instructions for that on the [recon-ng wiki](https://bitbucket.org/LaNMaSteR53/recon-ng/wiki/Usage%20Guide#!scripting-the-framework).

Script to enumerate subdomains, leveraging recon-ng. `enumall` uses the following tools to find subdomains and resolve IP:

* google scraping
* bing scraping
* baidu scraping
* yahoo scraping
* netcraft
* bruteforce

## Pre-Requisites

1. Clone the [Recon-ng][recon-ng] repository

   ```bash
   git clone https://LaNMaSteR53@bitbucket.org/LaNMaSteR53/recon-ng.git
   ```

2. Change into the Recon-ng directory.

    ```bash
    cd recon-ng
    ```

3. Install dependencies.

    ```bash
    pip install -r REQUIREMENTS
    ```

4. (optional) link the installation directory to `/usr/share/recon-ng`

    ```bash
    ln -s /$recon-ng_path /usr/share/recon-ng
    ```

5. (optional, but highly recommended) download: 

    + [altdns][altdns]
    + a good subdomain bruteforce list such as [danielmiessler/SecLists's sorted_knock_dnsrecon_fierce_recon-ng.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/sorted_knock_dnsrecon_fierce_recon-ng.txt)

6. Create `config.py` file and specify the path to `recon-ng` and `altdns` as shown in [`config_sample.py`](config_sample.py)

## Basic Usage

```bash
./enumall.py domain.com
```

Optional arguments:
+ `-w` to run a custom wordlist with recon-ng
+ `-a` to use altdns
+ `-p` to feed a custom permutations list to altdns (requires `-a` flag)
+ `-i` to feed a list of domains (can also type extra domains into the original command)

## Advanced Usage

```bash
./enumall.py domain1.com domain2.com domain3.com -i domainlist.txt -a -p permutationslist.txt -w wordlist.com
```

Output from recon-ng will be in `.lst` and `.csv` files, output from alt-dns will be in a `.txt` file

## License

[MIT](LICENSE.md) © @jhaddix and @leifdreizler

[recon-ng]: https://bitbucket.org/LaNMaSteR53/recon-ng
[altdns]: https://github.com/infosec-au/altdns
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <poll.h>
#include <fcntl.h>
#include <string.h>
#include <linux/limits.h>
#include <sys/wait.h>

#define GPIO_DIR "/sys/class/gpio"

#define STR_MAX 16
#define DEFAULT_NO "2"
#define DEFAULT_EDGE "falling"
#define DEFAULT_CMD "/usr/local/bin/shutdown_srv"
#define DEFAULT_CONF_PATH "/usr/local/etc/gpio2cmd.conf"

#define MAX_ARG 5

// struct
struct setting {
	char no[STR_MAX];
	char edge[STR_MAX];
	char cmd[PATH_MAX];
};

enum {
	NO,
	EDGE,
	CMD,
	KEY_MAX
};

// config file's key
const char setting_key[KEY_MAX][16] = {
	"gpio",
	"edge",
	"command"
};

// prototype
void read_config(const char* path, struct setting *conf);

int main(int argc, char *argv[])
{
        int fd = 0;
	struct setting config;
	char path[PATH_MAX] = { '\0' };

	memset(&config, '\0', sizeof(struct setting));
	read_config(DEFAULT_CONF_PATH, &config);

	//printf("no   = %s\n", config.no);
	//printf("edge = %s\n", config.edge);
	//printf("cmd  = %s\n", config.cmd);

	// export
	if(snprintf(path, sizeof(path), "%s/%s", GPIO_DIR, "export") < 0 ) {
		perror("make export path\n");
	}

        fd = open(path, O_WRONLY);
	if(fd < 0) {
		perror("open export\n");
		return -1;
	}
        if(write(fd, config.no, strlen(config.no)) < strlen(config.no)) {
		perror("write export\n");
	}
        close(fd);

	// direction
	if(snprintf(path, sizeof(path), "%s/gpio%s/%s", GPIO_DIR, config.no, "direction") < 0 ) {
		perror("make direction path\n");
	}
        fd = open(path, O_WRONLY);
	if(fd < 0) {
		perror("open direction\n");
		return -1;
	}
        if(write(fd, "in", 2) < 2) {
		perror("write direction\n");
	}
        close(fd);

	// edge
	if(snprintf(path, sizeof(path), "%s/gpio%s/%s", GPIO_DIR, config.no, "edge") < 0 ) {
		perror("make edge path\n");
	}
        fd = open(path, O_WRONLY);
	if(fd < 0) {
		perror("open edge\n");
		return -1;
	}
        if(write(fd, config.edge, strlen(config.edge)) < strlen(config.edge)) {
		perror("write edge\n");
	}
        close(fd);

//        for (int loop=1; loop += 0; --loop) {
        for (;;) {
                unsigned char val;
                struct pollfd pfd;

		// value
		if(snprintf(path, sizeof(path), "%s/gpio%s/%s", GPIO_DIR, config.no, "value") < 0 ) {
			perror("make value path\n");
		}
                fd = open(path, O_RDWR);
		if(fd < 0) {
			perror("open value\n");
			return -1;
		}
                if(read(fd, &val, 1) < 1) {
			perror("read valuer\n");
		}

		// poll
                pfd.fd = fd;
                pfd.events = POLLPRI;
                pfd.revents = 0;
                poll(&pfd, 1, -1);

                lseek(fd, 0, SEEK_SET);
                if(read(fd, &val, 1) < 1) {
			perror("read value\n");
		}
                close(fd);

		// exec command
		pid_t pid = fork();
		if(pid <0) {
			perror("fork\n");
			break;
		} else if(pid == 0) {	// child process
			char *ptr[MAX_ARG] = { NULL };
			int i = 0;
			ptr[i] = strtok(config.cmd, " ");
			while((ptr[i] != NULL) && i < MAX_ARG-1) {
				++i;
				ptr[i] = strtok(NULL, " ");
			}

			// http://manpages.ubuntu.com/manpages/trusty/ja/man3/execl.3.html
			// max 5 argument(=MAX_ARG)
			execlp(ptr[0], ptr[0], ptr[1], ptr[2], ptr[3], ptr[4], NULL);
			perror("execlp\n");
			exit(-1);
		}

		int status;
		pid_t ret = waitpid(pid, &status, 0);
		if(ret < 0) {
			perror("waitpid\n");
			break;
		}
		if(WIFEXITED(status)) {
			// success
		} else {
			perror("child process\n");
		}
        }

	// unexport
	if(snprintf(path, sizeof(path), "%s/%s", GPIO_DIR, "unexport") < 0 ) {
		perror("make unexport path\n");
	}
        fd = open(path, O_WRONLY);
	if(fd < 0) {
		perror("open unexport\n");
		return -1;
	}
        if(write(fd, config.no, strlen(config.no)) < strlen(config.no)) {
		perror("write unexport\n");
	}
        close(fd);

        return 0;
}

void read_config(const char* path, struct setting *conf)
{
	FILE *fp = NULL;
	fp = fopen(path, "rt");
	if(fp == NULL) {
		snprintf(conf->no, sizeof(conf->no), "%s", DEFAULT_NO);
		snprintf(conf->edge, sizeof(conf->edge), "%s", DEFAULT_EDGE);
		snprintf(conf->cmd, sizeof(conf->cmd), "%s", DEFAULT_CMD);
		return;
	}
	char str[PATH_MAX] = { '\0' };
	char *setting[3] = { conf->no, conf->edge, conf->cmd };
	unsigned int setting_len[3] = { sizeof(conf->no)-1, sizeof(conf->edge)-1, sizeof(conf->cmd)-1 };
	while(fgets(str, sizeof(str), fp) != NULL ) {
		for(int index=0; index<KEY_MAX; ++index) {
			if(strncmp(str, setting_key[index], strlen(setting_key[index])) == 0) {	// key find
				int i=0;
				int j=0;
				while (str[i++] != '=') {}	// skip until '='
				while (str[i] == ' ') {++i;}	// skip ' '
				while ((str[i] != '\n') && (j < setting_len[index])) {
					setting[index][j++] = str[i++];
				}
				setting[index][j] = '\0';
				break;
			}
		}
	}
	fclose(fp);
}

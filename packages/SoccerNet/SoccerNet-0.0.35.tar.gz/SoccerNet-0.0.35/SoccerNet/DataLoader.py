
from .utils import getListTestGames, getListGames



class VideoLoader():
    def __init__(self, SoccerNetDir, split="v1"):
        self.SoccerNetDir = SoccerNetDir
        self.split = split
        if split == "v1":
            self.listGame = getListGames()
        elif split == "test":
            self.listGame = getListTestGames()
        else:
            self.listGame = getListGames(split)

    def __len__(self):
        return len(self.listGame)

    def __iter__(self, index):
        video_path = self.listGame[index]

        # Read RELIABLE lenght for the video, in second
        if args.verbose:
            print("video path", video_path)
        v = cv2.VideoCapture(video_path)
        v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        time_second = v.get(cv2.CAP_PROP_POS_MSEC)/1000
        if args.verbose:
            print("duration video", time_second)
        import json
        metadata = skvideo.io.ffprobe(video_path)
        # print(metadata.keys())
        # print(json.dumps(metadata["video"], indent=4))
        # getduration
        # print(metadata["video"]["@avg_frame_rate"])
        # # print(metadata["video"]["@duration"])

        # Knowing number of frames from FFMPEG metadata w/o without iterating over all frames
        videodata = skvideo.io.FFmpegReader(video_path)
        (numframe, _, _, _) = videodata.getShape()  # numFrame x H x W x channels
        if args.verbose:
            print("shape video", videodata.getShape())

        # # extract REAL FPS
        fps_video = metadata["video"]["@avg_frame_rate"]
        fps_video = float(fps_video.split("/")[0])/float(fps_video.split("/")[1])
        # fps_video = numframe/time_second
        if args.verbose:
            print("fps=", fps_video)
        time_second = numframe / fps_video
        if args.verbose:
            print("duration video", time_second)
        frames = []
        videodata = skvideo.io.vreader(video_path)
        fps_desired = 2
        drop_extra_frames = fps_video/fps_desired
        for i_frame, frame in tqdm(enumerate(videodata), total=numframe):
            # print(i_frame % drop_extra_frames)
            if (i_frame % drop_extra_frames < 1):

                if args.preprocess == "resize256crop224":  # crop keep the central square of the frame
                    frame = imutils.resize(frame, height=256)  # keep aspect ratio
                    # number of pixel to remove per side
                    off_side_h = int((frame.shape[0] - 224)/2)
                    off_side_w = int((frame.shape[1] - 224)/2)
                    frame = frame[off_side_h:-off_side_h,
                                off_side_w:-off_side_w, :]  # remove them

                elif args.preprocess == "crop":  # crop keep the central square of the frame
                    frame = imutils.resize(frame, height=224)  # keep aspect ratio
                    # number of pixel to remove per side
                    off_side = int((frame.shape[1] - 224)/2)
                    frame = frame[:, off_side:-off_side, :]  # remove them

                elif args.preprocess == "resize":  # resize change the aspect ratio
                    # lose aspect ratio
                    frame = cv2.resize(frame, (224, 224),
                                    interpolation=cv2.INTER_CUBIC)

                else:
                    raise NotImplmentedError()
                frames.append(frame)

        # create numpy aray (nb_frames x 224 x 224 x 3)
        frames = np.array(frames)
        return frames
